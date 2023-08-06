# SimpleSplit
# by @fakerybakery
# https://github.com/fakerybakery/simplesplit
# Feel free to bundle this into your software, but please leave this attribution.
# Please make it clear if you change this program if you redistribute it.
# Please don't license this software under a different license or sublicense it.
# This software may be included in commercial software and/or other software as long as this package does not make up a significant portion of the software or is part of the core functionality.
# THE LICENSE AND ANY ASSOCIATED SOFTWARE, DOCUMENTATION, OR SERVICES ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. THE ENTIRE RISK ARISING OUT OF THE USE OR PERFORMANCE OF THE LICENSE, SOFTWARE, DOCUMENTATION, OR SERVICES REMAINS WITH THE LICENSEE. IN NO EVENT SHALL THE LICENSOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE LICENSE, SOFTWARE, DOCUMENTATION, OR SERVICES, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# v1.0.0
"""
SimpleSplit
https://github.com/fakerybakery/simplesplit
Usage:

python3 simplesplit.py split --input large_file --output nonexistent_directory

python3 simplesplit.py split --input large_file --output nonexistent_directory --chunk 1GB

python3 simplesplit.py combine --input some_directory --output nonexistent_output_file
"""
import argparse
import os
import sys
from tqdm import tqdm


def split_binary_file(file_path, output_dir, chunk_size):
    if os.path.isdir(output_dir):
        print(f"Error: {output_dir} already exists!")
        sys.exit(0)
    else:
        os.mkdir(output_dir)
    file_size = os.path.getsize(file_path)
    num_chunks = file_size // chunk_size + 1
    with open(file_path, 'rb') as file:
        with tqdm(total=num_chunks, unit='chunk') as pbar:
            chunk_number = 0
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                chunk_file_path = os.path.join(output_dir, f'simplesplit.{chunk_number}.ssc')
                with open(chunk_file_path, 'wb') as chunk_file:
                    chunk_file.write(data)
                chunk_number += 1
                pbar.update(1)
        print(f'File split into {chunk_number} chunks.')


def combine_chunks(directory, output_file):
    chunk_number = 0
    total_chunks = get_total_chunks(directory)
    if total_chunks == 0:
        print(f'Error: {directory} is not a SimpleSplit directory!')
        sys.exit(0)
    with open(output_file, 'wb') as file:
        pbar = tqdm(total=total_chunks, unit='chunk')
        while chunk_number < total_chunks:
            chunk_file_path = os.path.join(directory, f'siplesplit.{chunk_number}.ssc')
            try:
                with open(chunk_file_path, 'rb') as chunk_file:
                    data = chunk_file.read()
                    file.write(data)
                chunk_number += 1
                pbar.update(1)
            except FileNotFoundError:
                break
        pbar.close()
    print(f'File re-combined successfully.')


def get_total_chunks(directory):
    total_chunks = 0
    while True:
        chunk_file_path = os.path.join(directory, f'simplesplit.{total_chunks}.ssc')
        if os.path.exists(chunk_file_path):
            total_chunks += 1
        else:
            break
    return total_chunks


def main():
    parser = argparse.ArgumentParser(prog='simplesplit', description='Split and re-combine large binary files')
    subparsers = parser.add_subparsers(dest='command', required=True)

    split_parser = subparsers.add_parser('split', help='Split a binary file')
    split_parser.add_argument('--input', metavar='FILE', required=True, help='File to split')
    split_parser.add_argument('--output', metavar='DIRECTORY', required=True, help='Output directory')
    split_parser.add_argument('--chunk', metavar='SIZE', default='10MB', help='Chunk size (default: 10MB)')

    combine_parser = subparsers.add_parser('combine', help='Combine split files')
    combine_parser.add_argument('--input', metavar='DIRECTORY', required=True, help='Directory containing split files')
    combine_parser.add_argument('--output', metavar='FILE', required=True, help='Output file')

    args = parser.parse_args()

    if args.command == 'split':
        file_path = args.input
        output_dir = args.output
        chunk_size = parse_size(args.chunk)
        split_binary_file(file_path, output_dir, chunk_size)
    elif args.command == 'combine':
        directory = args.input
        output_file = args.output
        combine_chunks(directory, output_file)


def parse_size(size_str):
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 * 1024,
        'GB': 1024 * 1024 * 1024,
    }
    size_str = size_str.upper().replace(' ', '')
    for suffix, multiplier in multipliers.items():
        if size_str.endswith(suffix):
            size = size_str[:-len(suffix)]
            if size.isdigit():
                return int(size) * multiplier
    raise ValueError(f'Invalid size format: {size_str}')


if __name__ == '__main__':
    main()
