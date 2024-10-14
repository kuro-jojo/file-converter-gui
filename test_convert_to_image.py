import unittest
from unittest.mock import patch, MagicMock
from convert_to_image import convert_to_image, from_image, from_pdf


class TestConvertToImage(unittest.TestCase):

    @patch("os.path.exists")
    def test_convert_to_image_file_not_found(self, mock_exists):
        mock_exists.return_value = False

        result = convert_to_image("png", "jpg", "non_existent.png", "output.jpg")
        self.assertEqual(result, -1)

    @patch("os.path.exists")
    def test_convert_to_image_from_image_failure_same_type(self, mock_exists):
        image_format_expected = ["png", "jpg", "jpeg", "gif"]
        mock_exists.return_value = True
        for image_format in image_format_expected:
            result = convert_to_image(
                image_format,
                image_format,
                "example." + image_format,
                "output." + image_format,
            )
            self.assertEqual(result, -1)

    @patch("os.path.exists")
    @patch("convert_to_image.from_image")
    def test_convert_to_image_from_image_success(self, mock_from_image, mock_exists):
        image_format_expected = ["png", "jpg", "jpeg", "gif"]
        mock_exists.return_value = True
        mock_from_image.return_value = 0
        for input_format in image_format_expected:
            for output_format in image_format_expected:
                if input_format != output_format:
                    result = convert_to_image(
                        input_format,
                        output_format,
                        "example." + input_format,
                        "output." + output_format,
                    )
                    self.assertEqual(result, 0)
                    mock_from_image.assert_called_with(
                        "example." + input_format, "output." + output_format
                    )

    @patch("os.path.exists")
    @patch("convert_to_image.from_pdf")
    def test_convert_to_image_from_pdf_success(self, mock_from_pdf, mock_exists):
        image_format_expected = ["png", "jpg", "jpeg", "gif"]
        mock_exists.return_value = True
        mock_from_pdf.return_value = 0
        for output_format in image_format_expected:
            result = convert_to_image(
                "pdf", output_format, "example.pdf", "output." + output_format
            )
            self.assertEqual(result, 0)
            mock_from_pdf.assert_called_with(
                "example.pdf", "", "example", output_format
            )

    @patch("PIL.Image.open")
    def test_from_image_success(self, mock_open):
        mock_image = MagicMock()
        mock_converted_image = MagicMock()

        mock_open.return_value.__enter__.return_value = mock_image
        mock_image.convert.return_value = mock_converted_image

        result = from_image("example.png", "output.jpg")
        self.assertEqual(result, 0)
        mock_image.convert.assert_called_once_with("RGB")
        mock_converted_image.save.assert_called_once_with("output.jpg")

    @patch("pdf2image.convert_from_path")
    def test_from_pdf_no_images_created(self, mock_convert_from_path):
        mock_convert_from_path.return_value = []

        result = from_pdf("example.pdf", "", "example", "png")
        self.assertEqual(result, -1)

    @patch("pdf2image.convert_from_path")
    def test_from_pdf_success_single_image(self, mock_convert_from_path):
        mock_image = MagicMock()
        mock_convert_from_path.return_value = [mock_image]

        result = from_pdf("example.pdf", "", "example", "png")
        self.assertEqual(result, 0)
        mock_image.save.assert_called_once_with("example.png")

    @patch("pdf2image.convert_from_path")
    def test_from_pdf_success_multiple_images(self, mock_convert_from_path):
        mock_images = [MagicMock(), MagicMock()]
        mock_convert_from_path.return_value = mock_images

        result = from_pdf("example.pdf", "", "example", "png")
        self.assertEqual(result, 0)
        mock_images[0].save.assert_called_once_with("example_1.png")
        mock_images[1].save.assert_called_once_with("example_2.png")


if __name__ == "__main__":
    unittest.main()
