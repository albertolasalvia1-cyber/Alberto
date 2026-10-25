#!/usr/bin/env bash
# Rilevamento silenzi adattivo (loudnorm + silencedetect) e taglio automatico.
# Uso: taglia-silenzi.sh input.mp4 [output.mp4] [durata_min_silenzio=0.5] [margine=0.15]
set -euo pipefail

IN="$1"
OUT="${2:-${IN%.*}_senza_silenzi.mp4}"
MIN_DUR="${3:-0.5}"
PAD="${4:-0.15}"   # secondi di respiro lasciati prima/dopo ogni parte parlata

if [ "$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | wc -l)" -eq 0 ]; then
  echo "ERRORE: '$IN' non ha traccia audio, impossibile rilevare i silenzi." >&2
  exit 1
fi

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")

# Step 1: soglia adattiva dal gating EBU R128
THRESH=$(ffmpeg -hide_banner -i "$IN" -map 0:a:0 -af loudnorm=print_format=json -f null /dev/null 2>&1 \
  | grep '"input_thresh"' | sed -E 's/.*"(-?[0-9.]+|-inf)".*/\1/')
[ "$THRESH" = "-inf" ] && THRESH=-50
echo "Soglia silenzio: ${THRESH} dB (durata minima ${MIN_DUR}s)"

# Step 2: silencedetect
SIL=$(ffmpeg -hide_banner -i "$IN" -map 0:a:0 -af "silencedetect=noise=${THRESH}dB:d=${MIN_DUR}" -f null /dev/null 2>&1 \
  | grep -oE 'silence_(start|end): -?[0-9.]+' | awk '{print $2}')

# Step 3: calcola i segmenti da tenere (complementari ai silenzi, con margine)
SEGS=$(echo "$SIL" | awk -v dur="$DUR" -v pad="$PAD" '
  { v[NR]=$1 }
  END {
    cur=0; n=0
    for (i=1; i<=NR; i+=2) {
      s=v[i]; e=(i+1<=NR)?v[i+1]:dur
      a=cur; b=s+pad; if (b>dur) b=dur
      if (b-a>2*pad+0.05) printf "%.3f %.3f\n", a, b
      cur=e-pad; if (cur<0) cur=0
    }
    if (dur-cur>2*pad+0.05) printf "%.3f %.3f\n", cur, dur
  }')

echo "Silenzi trovati: $(( $(echo "$SIL" | grep -c . || true) / 2 ))"
echo "Segmenti tenuti:"; echo "$SEGS"

# Step 4: taglio preciso con trim/concat (ricodifica)
HAS_V=$(ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 "$IN" | wc -l)
FILTER=""; LABELS=""; i=0
while read -r a b; do
  [ -z "$a" ] && continue
  if [ "$HAS_V" -gt 0 ]; then
    FILTER+="[0:v]trim=${a}:${b},setpts=PTS-STARTPTS[v$i];"
    LABELS+="[v$i]"
  fi
  FILTER+="[0:a]atrim=${a}:${b},asetpts=PTS-STARTPTS[a$i];"
  LABELS+="[a$i]"
  i=$((i+1))
done <<< "$SEGS"

if [ "$HAS_V" -gt 0 ]; then
  FILTER+="${LABELS}concat=n=$i:v=1:a=1[v][a]"
  ffmpeg -hide_banner -loglevel error -y -i "$IN" -filter_complex "$FILTER" -map "[v]" -map "[a]" \
    -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  FILTER+="${LABELS}concat=n=$i:v=0:a=1[a]"
  ffmpeg -hide_banner -loglevel error -y -i "$IN" -filter_complex "$FILTER" -map "[a]" "$OUT"
fi

NEW=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
printf "Fatto: %s  (%.1fs -> %.1fs)\n" "$OUT" "$DUR" "$NEW"
