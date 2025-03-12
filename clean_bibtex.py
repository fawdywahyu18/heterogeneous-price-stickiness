# Script untuk cek dan mengahpus artikel yang duplikat di file Bibtex

from pybtex.database import parse_file, BibliographyData, Entry
import sys

def remove_duplicates(input_file, output_file):
    try:
        # Parse BibTeX file
        bib_data = parse_file(input_file)
        
        # Dictionary to store unique entries based on (title, doi)
        unique_entries = {}
        
        for key, entry in bib_data.entries.items():
            title = entry.fields.get('title', '').strip().lower()
            doi = entry.fields.get('doi', '').strip().lower() if 'doi' in entry.fields else None
            
            identifier = (title, doi)
            
            if identifier not in unique_entries:
                unique_entries[identifier] = entry
        
        # Create new BibTeX database with unique entries
        new_bib_data = BibliographyData(entries={f'entry{i}': entry for i, entry in enumerate(unique_entries.values(), 1)})
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_bib_data.to_string('bibtex'))
        
        print(f"Processed {len(bib_data.entries)} entries. Removed {len(bib_data.entries) - len(unique_entries)} duplicates.")
        print(f"Cleaned file saved as: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_duplicates.py input.bib output.bib")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        remove_duplicates(input_file, output_file)
