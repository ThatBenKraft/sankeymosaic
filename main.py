from pathlib import Path

from PIL import Image

DEFAULT_SCALE = 100

def main() -> None:
        
    directory_path = Path(__file__).parent
    # Opens settings file to read
    with open(directory_path / "settings.txt") as settings_file:
        # Opens output file to write
        with open(directory_path / "output.txt", "w") as output_file:
            # Opens image file to read
            with Image.open(directory_path / "sample.png") as image:
                # Writes custom image data to output file
                output_file.writelines(get_flows(image))
            # Writes default settings to output file
            output_file.writelines(settings_file.readlines())



def get_flows(image: Image.Image, scale: int = DEFAULT_SCALE) -> list[str]:
    """
    Gets custom data from image and converts to flow data.
    """
    custom_lines = []

    custom_lines.append("D [1] E\nE [1] F\n\n")

    width, height = (axis * scale for axis in image.size)
    custom_lines.append(f"size w {width}\n  h {height}\n")

    return custom_lines


if __name__ == "__main__":
    main()