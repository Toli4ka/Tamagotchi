from pathlib import Path

def pbm_to_bytes(pbm_file):
    """Convert a PBM file to a byte array."""
    with open(pbm_file, 'rb') as f:
        # Read the PBM header
        header = f.readline().strip()
        if header != b'P4':
            raise ValueError("Not a valid PBM file")
        
        # Read lines until we get the dimensions (skip comments)
        while True:
            line = f.readline()
            if not line:
                raise ValueError("Unexpected end of file.")
            line = line.strip()
            if line.startswith(b'#'):
                continue
            else:
                dimensions = line
                break
        width, height = map(int, dimensions.split())
        
        # The rest is pixel data
        pixel_data = f.read()
    
    return pixel_data, width, height

if __name__ == "__main__":
    pbm_file_path = Path('cat4.pbm')
    if pbm_file_path.exists():
        byte_array, width, height = pbm_to_bytes(pbm_file_path)
        print(f"Width: {width}, Height: {height}")
        print(f"Byte array for {pbm_file_path}: {list(byte_array)}")
    else:
        print(f"File {pbm_file_path} does not exist.")