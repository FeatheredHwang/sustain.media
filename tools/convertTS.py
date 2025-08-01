from opencc import OpenCC
# converter = OpenCC('t2s.json')
# t = converter.convert('漢字')  # 汉字
# print(t)

def convert_traditional_to_simplified(input_path: str, output_path: str) -> None:
    """
    Convert a text file from Traditional Chinese to Simplified Chinese using OpenCC.

    Args:
        input_path (str): Path to the Traditional Chinese input file.
        output_path (str): Path to save the Simplified Chinese output file.
    """
    cc = OpenCC('t2s')  # 't2s' means Traditional to Simplified
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            simplified_line = cc.convert(line)
            outfile.write(simplified_line)

# Example usage:
convert_traditional_to_simplified('traditional.txt', 'simplified.txt')