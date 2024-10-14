def convert_to_pdf(file_type: str, file_path: str, output_file: str) -> int:
    """
    Converts a file to PDF format.

    Args:
        file_type (str): The type of the file to convert. Supported types are 'img' for images and 'doc' for Word documents.
        file_path (str): The path to the input file that needs to be converted.
        output_file (str): The desired path for the output PDF file. If not provided, the output file will have the same name as the input file with a .pdf extension.

    Returns:
        int: Returns 0 on successful conversion, -1 if the file does not exist or if the file type is unsupported.
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
        output_file = file_name.removesuffix(file_extension) + "pdf"

    if not output_file.endswith(".pdf"):
        output_file = output_file + ".pdf"

    output_file = output_path + output_file

    match file_type:
        case "img":
            return from_image(file_path, output_file)
        case "doc":
            return from_word(file_path, output_file)

    return -1


def from_image(image_file: str, output_file: str) -> int:
    """
    Converts an image file to a PDF file.

    Args:
        image_file (str): The path to the input image file. Supported formats are 'png', 'jpg', 'jpeg', 'gif'.
        output_file (str): The path to the output PDF file.

    Returns:
        int: Returns 0 if the conversion is successful, -1 if the image file is not found or if the file format is not supported.

    Raises:
        FileNotFoundError: If the image file is not found.
    """
    from PIL import Image

    image_extensions = ["png", "jpg", "jpeg", "gif"]

    if image_file.split(".")[-1] not in image_extensions:
        print("Image file must be one of the following types: ", image_extensions)
        return -1

    try:
        with Image.open(image_file) as im:
            im = im.convert("RGB")
            im.save(output_file)
    except FileNotFoundError:
        print("Image file not found")
        return -1

    return 0


def from_word(word_file: str, output_file: str) -> int:
    """
    Converts a Word document to a PDF file.

    Args:
        word_file (str): The path to the input Word document. Must have a .doc or .docx extension.
        output_file (str): The path where the output PDF file will be saved.

    Returns:
        int: Returns 0 if the conversion is successful, -1 if the input file is not a valid Word document.
    """
    from spire.doc import Document, FileFormat

    word_extensions = ["doc", "docx"]
    file_extension = word_file.split(".")[-1]
    if file_extension not in word_extensions:
        print("word file must be one of the following types: ", word_extensions)
        return -1

    # Create word document
    document = Document()
    document.LoadFromFile(word_file)
    document.SaveToFile(output_file, FileFormat.PDF)
    document.Close()

    return 0