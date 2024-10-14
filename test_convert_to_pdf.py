import unittest
from unittest.mock import patch, mock_open, MagicMock
import os

from convert_to_pdf import convert_to_pdf, from_image, from_word


class TestConvertToPdf(unittest.TestCase):

    @patch("os.path.exists")
    def test_convert_to_pdf_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        result = convert_to_pdf("img", "non_existent_file.png", "output.pdf")
        self.assertEqual(result, -1)

    @patch("os.path.exists")
    @patch("convert_to_pdf.from_image")
    def test_convert_to_pdf_image_success(self, mock_from_image, mock_exists):
        mock_exists.return_value = True
        mock_from_image.return_value = 0
        result = convert_to_pdf("img", "example.png", "output.pdf")
        self.assertEqual(result, 0)
        mock_from_image.assert_called_once_with("example.png", "output.pdf")

    @patch("os.path.exists")
    @patch("convert_to_pdf.from_word")
    def test_convert_to_pdf_word_success(self, mock_from_word, mock_exists):
        mock_exists.return_value = True
        mock_from_word.return_value = 0
        result = convert_to_pdf("doc", "example.docx", "output.pdf")
        self.assertEqual(result, 0)
        mock_from_word.assert_called_once_with("example.docx", "output.pdf")

    @patch("os.path.exists")
    def test_convert_to_pdf_invalid_type(self, mock_exists):
        mock_exists.return_value = True
        result = convert_to_pdf("invalid", "example.txt", "output.pdf")
        self.assertEqual(result, -1)

    @patch("PIL.Image.open")
    def test_from_image_success(self, mock_open):
        mock_image = MagicMock()
        mock_converted_image = MagicMock()
        
        mock_open.return_value.__enter__.return_value = mock_image
        mock_image.convert.return_value = mock_converted_image

        result = from_image("example.png", "output.pdf")
        self.assertEqual(result, 0)
        mock_image.convert.assert_called_once_with("RGB")
        mock_converted_image.save.assert_called_once_with("output.pdf")

    def test_from_image_invalid_extension(self):
        result = from_image("example.txt", "output.pdf")
        self.assertEqual(result, -1)

    @patch("PIL.Image.open")
    def test_from_image_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError
        result = from_image("non_existent.png", "output.pdf")
        self.assertEqual(result, -1)

    @patch("spire.doc.FileFormat")
    @patch("spire.doc.Document")
    def test_from_word_success(self, mock_document, mock_format):
        mock_doc_instance = mock_document.return_value
        mock_format.PDF = MagicMock()
        result = from_word("example.docx", "output.pdf")
        self.assertEqual(result, 0)
        mock_doc_instance.LoadFromFile.assert_called_once_with("example.docx")
        mock_doc_instance.SaveToFile.assert_called_once_with("output.pdf", mock_format.PDF)
        mock_doc_instance.Close.assert_called_once()

    def test_from_word_invalid_extension(self):
        result = from_word("example.txt", "output.pdf")
        self.assertEqual(result, -1)


if __name__ == "__main__":
    unittest.main()
