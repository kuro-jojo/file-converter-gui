def convert_to_pdf(file_type: str, file_path: str, output_file: str) -> int:
    import os

    """
    Converts a file to PDF format based on the specified file type.

    Args:
        file_type (str): The type of the file to be converted. Supported types are "img" and "doc".
        file_path (str): The name of the input file to be converted.
        output_file (str): The name of the output PDF file.

    Returns:
        int: A status code indicating the result of the conversion. Typically, 0 for success and non-zero for failure.
    """
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


def from_word(word_file: str, output_file: str) -> int:
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


