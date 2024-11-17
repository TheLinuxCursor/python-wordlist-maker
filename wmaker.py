import os
import itertools
import time

def generate_and_save_wordlist(chrs, min_len, max_len, total_combinations, output_file, batch_size=1000, update_interval=1000):
    current_count = 0
    start_time = time.time()

    with open(output_file, 'w') as file:
        for n in range(min_len, max_len + 1):
            batch = []
            for xs in itertools.product(chrs, repeat=n):
                batch.append(''.join(xs))
                current_count += 1

                if len(batch) >= batch_size:
                    file.write('\n'.join(batch) + '\n')
                    batch.clear()

                if current_count % update_interval == 0 or current_count == total_combinations:
                    elapsed_time = time.time() - start_time
                    words_per_second = current_count / elapsed_time
                    remaining_time = (total_combinations - current_count) / words_per_second if words_per_second > 0 else 0
                    remaining_time_formatted = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
                    percent = (current_count * 100) // total_combinations
                    print(f"Progress: {percent}% ({current_count}/{total_combinations}) | Time Remaining: {remaining_time_formatted}", end='\r', flush=True)

            if batch:
                file.write('\n'.join(batch) + '\n')

    print("\nDone!")

def get_file_size(file_path):
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        units = ["Bytes", "KB", "MB", "GB", "TB"]
        unit_index = 0
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        return size, f"{size:.2f} {units[unit_index]}"
    return 0, "0 Bytes"

def estimate_file_size(chrs, min_len, max_len):
    total_combinations = sum(len(chrs) ** n for n in range(min_len, max_len + 1))
    estimated_size = total_combinations * (max_len + 1)
    return total_combinations, estimated_size

def format_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size //= 1024
        unit_index += 1
    return f"{size} {units[unit_index]}"

# Main script logic
chrs = input("Enter characters to make wordlist: ")

try:
    min_len = int(input("Enter the minimum length of words: "))
    max_len = int(input("Enter the maximum length of words: "))
    output_file = input("Enter the file name to save the wordlist (e.g., wordlist.txt): ")
    total_combinations, estimated_size = estimate_file_size(chrs, min_len, max_len)
    print(f"Estimated wordlist size with {total_combinations} combinations:")
    print(f"Estimated file size: {format_size(estimated_size)}")
    if min_len > max_len:
        raise ValueError("Minimum length cannot be greater than maximum length!")

    proceed = input(f"Do you want to generate and save the wordlist? (Y/n): ").strip().lower()

    if proceed == '' or proceed == 'y':
        print(f"Generating wordlist from length {min_len} to {max_len} and saving to '{output_file}'...")
        generate_and_save_wordlist(chrs, min_len, max_len, total_combinations, output_file)
        final_size, final_size_hr = get_file_size(output_file)
        print(f"\nWordlist has been successfully saved to '{output_file}'.")
    else:
        print("Wordlist generation has been canceled.")

except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
