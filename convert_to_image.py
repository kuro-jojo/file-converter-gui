def convert_to_image(
    file_type: str, output_type: str, file_path: str, output_file: str
) -> int:
    """
    Converts a file to an image of the specified output type.

    Args:
        file_type (str): The type of the input file (e.g., 'png', 'jpg', 'jpeg', 'gif', 'pdf').
        output_type (str): The desired output image type (e.g., 'png', 'jpg', 'jpeg', 'gif').
        file_path (str): The path to the input file.
        output_file (str): The path to the output file. If not provided, it will be generated based on the input file name and output type.

    Returns:
        int: Returns 0 on success, -1 on failure (e.g., if the file does not exist or the conversion type is invalid).

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the output type is the same as the input file type.
    """
    import os

    if not os.path.exists(file_path):
        print(f"{file_path} not found")
        return -1

    file_name = (
        file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
    )
    output_path = file_path.removesuffix(file_name)
    file_extension = file_name.split(".")[-1]

    if not output_file:
        output_file = file_name.removesuffix(file_extension) + output_type

    if not output_file.endswith(output_type):
        output_file = output_file + "." + output_type

    output_file = output_path + output_file

    match file_type:
        case "png" | "jpg" | "jpeg" | "gif":
            if file_extension == output_type:
                print("The converted type must be different from the original type")
                return -1
            return from_image(file_path, output_file)
        case "pdf":
            return from_pdf(
                file_path, output_path, file_name.removesuffix(".pdf"), output_type
            )

    return -1


def from_image(image_file: str, output_file: str) -> int:
    """
    Converts an image file to a different format and saves it to the specified output file.

    Args:
        image_file (str): The path to the input image file. Must be one of the following types: png, jpg, jpeg, gif.
        output_file (str): The path to the output file where the converted image will be saved.

    Returns:
        int: Returns 0 if the conversion is successful, -1 if the input file is not an image or if the file is not found.

    Raises:
        FileNotFoundError: If the input image file does not exist.
    """
    from PIL import Image

    image_extensions = ["png", "jpg", "jpeg", "gif"]

    if image_file.split(".")[-1] not in image_extensions:
        print("Image file must be one of the following types: ", image_extensions)
        return -1

    try:
        with Image.open(image_file) as im:
            image = im.convert("RGB")
            image.save(output_file)
    except FileNotFoundError:
        print("Image file not found")
        return -1

    return 0


def from_pdf(
    pdf_file: str, output_path: str, file_name_without_ext: str, output_type: str
) -> int:
    """
    Converts a PDF file to images and saves them to the specified output path.

    Args:
        pdf_file (str): The path to the PDF file to be converted.
        output_path (str): The directory where the output images will be saved.
        file_name_without_ext (str): The base name for the output image files, without extension.
        output_type (str): The image file format (e.g., 'png', 'jpg').

    Returns:
        int: Returns 0 if the conversion is successful, -1 if no images are created or if a FileNotFoundError occurs.
    """
    from pdf2image import convert_from_path

    images = convert_from_path(pdf_file)
    if not images:
        print("No images created")
        return -1

    try:
        if len(images) == 1:
            images[0].save(f"{output_path}{file_name_without_ext}.{output_type}")
        else:
            for i, image in enumerate(images):
                image.save(f"{output_path}{file_name_without_ext}_{i+1}.{output_type}")
    except FileNotFoundError:
        print("Image file not found")
        return -1

    return 0
