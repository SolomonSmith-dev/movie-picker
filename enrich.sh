#!/bin/bash

echo ""
echo "🎬 Movie Metadata Enricher"
echo "=========================="
echo "Choose a list to enrich:"
echo "1. Plex Movies"
echo "2. Greatest Movies"
echo ""

read -p "Enter 1 or 2: " choice

if [ "$choice" == "1" ]; then
  echo "✨ Enriching Plex Movies..."
  python3 metadata_enricher.py --input lists/plex_movies_final.json --output lists/plex_movies_enriched.json
elif [ "$choice" == "2" ]; then
  echo "✨ Enriching Greatest Movies..."
  python3 metadata_enricher.py --input lists/standardized_movies_final.json --output lists/standardized_movies_enriched.json
else
  echo "❌ Invalid choice."
fi
