import os
import concurrent.futures

def slide_window(seq, length=20):
    return [seq[i:i+length] for i in range(len(seq) - length + 1)]

def process_fasta_file(input_file, output_file):
    """
    Process the input FASTA file, slicing each sequence and outputting the results to a new FASTA file.
    
    :param input_file: Path to the input FASTA file
    :param output_file: Path to the output FASTA file
    """
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

def process_single_file(input_file, output_folder):
    output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_processed.fasta")
    process_fasta_file(input_file, output_file)
    print(f"Processed {input_file} and saved to {output_file}")

def process_all_fasta_files(input_folder, output_folder, num_workers=4):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fasta_files = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith('.fasta')]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_single_file, input_file, output_folder) for input_file in fasta_files]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing file: {e}")

# Example usage
input_folder = '/home/zxg/GMACID/seqtk1M'
output_folder = '/home/zxg/GMACID/cutkmer20'
num_workers = 4  # Set the number of threads based on available resources

process_all_fasta_files(input_folder, output_folder, num_workers)
