from pybtex.database import parse_file, BibliographyData
import sys
import re

def remove_duplicate_keys(input_file, temp_output_file):
    """
    Menghapus duplikasi berdasarkan kunci (BibTeX key) sebelum parsing.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        bib_lines = f.readlines()

    unique_keys = set()
    cleaned_lines = []
    inside_entry = False
    current_key = None

    for line in bib_lines:
        match = re.match(r'@\w+{([^,]+),', line)
        if match:
            current_key = match.group(1)
            if current_key in unique_keys:
                inside_entry = True  # Lewati entri ini karena duplikat
                print(f"Duplicate entry removed: {current_key}")
                continue
            unique_keys.add(current_key)
            inside_entry = False

        if not inside_entry:
            cleaned_lines.append(line)

    with open(temp_output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"Step 1: Removed duplicate keys. Cleaned file saved as: {temp_output_file}")

def generate_bibtex_key(entry):
    """
    Membuat kunci BibTeX berdasarkan nama author pertama dan tahun publikasi.
    """
    try:
        # Ambil daftar author dari pybtex
        authors = entry.persons.get('author', [])
        
        if authors:
            first_author = authors[0].last_names[0] if authors[0].last_names else "Unknown"
        else:
            first_author = "Unknown"

        # Ambil tahun
        year = entry.fields.get('year', '0000')

        # Buat kunci BibTeX
        bibtex_key = f"{first_author}{year}"
        return re.sub(r'[^a-zA-Z0-9]', '', bibtex_key)  # Hapus karakter tidak valid
    except Exception as e:
        print(f"Error generating key: {e}")
        return "Unknown0000"

def remove_duplicate_entries(input_file, output_file):
    """
    Menghapus entri duplikat berdasarkan title dan DOI, serta memberikan key berdasarkan nama author.
    """
    try:
        bib_data = parse_file(input_file)
        unique_entries = {}

        for key, entry in bib_data.entries.items():
            title = entry.fields.get('title', '').strip().lower()
            doi = entry.fields.get('doi', '').strip().lower() if 'doi' in entry.fields else None
            identifier = (title, doi)

            if identifier not in unique_entries:
                unique_key = generate_bibtex_key(entry)
                unique_entries[unique_key] = entry

        new_bib_data = BibliographyData(entries=unique_entries)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_bib_data.to_string('bibtex'))

        print(f"Step 2: Removed duplicate entries. Processed {len(bib_data.entries)} entries. Saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_duplicates.py input.bib output.bib")
    else:
        input_file = sys.argv[1]
        temp_file = "temp_cleaned.bib"
        output_file = sys.argv[2]

        remove_duplicate_keys(input_file, temp_file)
        remove_duplicate_entries(temp_file, output_file)
