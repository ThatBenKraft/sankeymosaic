from pathlib import Path
from typing import Callable

from PIL import Image

DEFAULT_SCALE = 7.5


def main() -> None:
    """
    Run main action of mosiac maker.
    """
    # Create directory path
    directory_path = Path(__file__).parent
    samples_path = directory_path / "assets" / "samples"

    while True:
        # Request image filename
        image_filename = input(f"Please enter image filename within samples folder: ")
        # Break if filename valid
        image_path = samples_path / image_filename
        if image_path.exists():
            break
        # Else report invalidity and loop
        print(
            f"Invalid filename. Check to see if '{image_filename}' is in {samples_path}.\n"
        )

    # Open output file to write
    with open(directory_path / "output.txt", "w") as output_file:
        # Open settings file to read
        with open(directory_path / "settings.txt") as settings_file:
            # Open image file to read
            with Image.open(image_path) as image:
                # Write custom image data to output file
                output_file.writelines(get_flows(image))
            # Copy default settings to output file
            output_file.writelines(settings_file.readlines())

    print(
        f"\nMosaic created using '{image_filename}'! Resulting Sankey input within 'output.txt'"
    )


def get_flows(image: Image.Image, scale: float = DEFAULT_SCALE) -> list[str]:
    """
    Get custom data from image and converts to flow data.
    """
    custom_lines = []
    # Get largest pixel ID possible
    max_id = len(str((image.width + 1) * image.height - 1))
    # Load pixel data from image
    pixels = image.load()

    id = 0
    # For each vertical pixel:
    for y in range(image.height):
        # For each horizontal pixel:
        for buffer in range(image.width):
            # Acquire RGB pixel from image data
            rgb_color: tuple[int, ...] = pixels[buffer, y]  # type: ignore
            # Remove transparency data and type checks
            if len(rgb_color) == 4:
                print("Trimming transparency data. . .")
                rgb_color = rgb_color[:3]
            elif len(rgb_color) != 3:
                raise TypeError("Image in is invalid format! Please use .png or .jpg")
            # Convert pixel color from RGB to HEX
            hex_color = "#%02x%02x%02x" % rgb_color  # type: ignore
            # Build string from ID to next with color
            custom_lines.append(
                f"{id:0{max_id}d} [1] {(id + 1):0{max_id}d} {hex_color}\n"
            )
            # Add to ID
            id += 1
        # Carriage return by starting from new ID
        custom_lines.append("\n")
        id += 1
    # Scale image width and height before adding to settings
    width, height = (int(axis * scale) for axis in image.size)
    custom_lines.append(f"size w {width}\n  h {height}\n")
    # Return built string list
    return custom_lines


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEnding mosaic!")
