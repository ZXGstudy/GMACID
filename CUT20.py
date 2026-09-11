import os
import concurrent.futures
from tqdm import tqdm

def slide_window(seq, length=20):
    return [seq[i:i+length] for i in range(len(seq) - length + 1)]

def process_fasta_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_header = None
        current_sequence = []
        
        for line in infile:
            line = line.strip()  
            if line.startswith('>'):
                # Process the previous sequence if it exists
                if current_header and current_sequence:
                    sequence = ''.join(current_sequence)
                    substrings = slide_window(sequence)
                    for i, substr in enumerate(substrings):
                        outfile.write(f">{current_header}_slice_{i+1}\n")
                        outfile.write(f"{substr}\n")
                # Start a new sequence
                current_header = line[1:]
                current_sequence = []
            else:
                current_sequence.append(line)
        
        # Process the last sequence in the file
        if current_header and current_sequence:
            sequence = ''.join(current_sequence)
            substrings = slide_window(sequence)
            for i, substr in enumerate(substrings):
                outfile.write(f">{current_header}_slice_{i+1}\n")
                outfile.write(f"{substr}\n")

def process_fastq_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        while True:
            header = infile.readline().strip()
            if not header:
                break
            sequence = infile.readline().strip()
            plus = infile.readline().strip()  # Skip this line
            quality = infile.readline().strip()  # Skip this line
            
            substrings = slide_window(sequence)
            
            for i, substr in enumerate(substrings):
                outfile.write(f">{header[1:]}_slice_{i+1}\n")
                outfile.write(f"{substr}\n")

def process_single_file(input_file, output_folder):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_folder, f"{base_name}_processed.fa")
    
    if input_file.endswith('.fa') or input_file.endswith('.fasta'):
        process_fasta_file(input_file, output_file)
    elif input_file.endswith('.fq') or input_file.endswith('.fastq'):
        process_fastq_file(input_file, output_file)
        
    print(f"Processed {input_file} and saved to {output_file}")

def process_all_sequence_files(input_folder, output_folder, num_workers=4):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sequence_files = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith(('.fa', '.fasta', '.fq', '.fastq'))]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_single_file, input_file, output_folder) for input_file in sequence_files]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing file: {e}")

# Example usage
input_folder = '/home/zxg/GMACID/TEST'
output_folder = '/home/zxg/GMACID/TEST/CUT20'
num_workers = 4  # Set the number of threads based on available resources

process_all_sequence_files(input_folder, output_folder, num_workers)
