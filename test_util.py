"""
Test suite for util.py — Shared utility helper functions.
Tests cover random hex generation, image resizing, EXIF orientation
correction, aspect ratio handling, and error cases.
"""

import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock
from PIL import Image


# ---------------------------------------------------------------------------
# Helpers - create test images in memory
# ---------------------------------------------------------------------------


def create_test_image(width, height, mode="RGB", color=(255, 0, 0)):
    """Create a simple in-memory test image and return it as a BytesIO object."""
    img = Image.new(mode, (width, height), color=color)
    stream = BytesIO()
    img.save(stream, format="PNG")
    stream.seek(0)
    return stream


def create_image_with_exif(width, height, orientation):
    """
    Create an in-memory JPEG image with a specific EXIF orientation tag.
    Uses piexif if available, otherwise patches _getexif directly.
    """
    img = Image.new("RGB", (width, height), color=(100, 150, 200))
    stream = BytesIO()

    try:
        import piexif

        exif_dict = {"0th": {piexif.ImageIFD.Orientation: orientation}}
        exif_bytes = piexif.dump(exif_dict)
        img.save(stream, format="JPEG", exif=exif_bytes)
    except ImportError:
        # Fallback: save without real EXIF and mock _getexif in tests
        img.save(stream, format="JPEG")

    stream.seek(0)
    return stream


# ---------------------------------------------------------------------------
# random_hex_bytes
# ---------------------------------------------------------------------------


class TestRandomHexBytes:

    def test_returns_string(self):
        """Should return a string."""
        import util

        result = util.random_hex_bytes(8)
        assert isinstance(result, str)

    def test_correct_length(self):
        """Should return a hex string of length 2 * n_bytes."""
        import util

        result = util.random_hex_bytes(8)
        assert len(result) == 16  # 8 bytes = 16 hex characters

    def test_correct_length_varied(self):
        """Should scale correctly for different byte counts."""
        import util

        for n in [4, 8, 16, 32]:
            result = util.random_hex_bytes(n)
            assert len(result) == n * 2

    def test_returns_valid_hex(self):
        """Should only contain valid hexadecimal characters."""
        import util

        result = util.random_hex_bytes(16)
        assert all(c in "0123456789abcdef" for c in result)

    def test_returns_different_values(self):
        """Should return different values on each call (random)."""
        import util

        result1 = util.random_hex_bytes(16)
        result2 = util.random_hex_bytes(16)
        assert result1 != result2


# ---------------------------------------------------------------------------
# resize_image - basic functionality
# ---------------------------------------------------------------------------


class TestResizeImageBasic:

    def test_returns_bytes_for_valid_image(self):
        """Should return bytes for a valid image input."""
        import util

        image_stream = create_test_image(200, 200)
        result = util.resize_image(image_stream, (120, 160))
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_output_is_valid_png(self):
        """Should return valid PNG bytes."""
        import util

        image_stream = create_test_image(200, 200)
        result = util.resize_image(image_stream, (120, 160))
        output = Image.open(BytesIO(result))
        assert output.format == "PNG"

    def test_output_matches_target_size(self):
        """Output image canvas should match the requested size exactly."""
        import util

        image_stream = create_test_image(400, 400)
        target_size = (120, 160)
        result = util.resize_image(image_stream, target_size)
        output = Image.open(BytesIO(result))
        assert output.size == target_size

    def test_returns_none_for_invalid_file(self):
        """Should return None when the input cannot be opened as an image."""
        import util

        bad_file = BytesIO(b"this is not an image")
        result = util.resize_image(bad_file, (120, 160))
        assert result is None


# ---------------------------------------------------------------------------
# resize_image - aspect ratio handling
# ---------------------------------------------------------------------------


class TestResizeImageAspectRatio:

    def test_wide_image_fits_within_target(self):
        """A wide image should be scaled to fit within the target dimensions."""
        import util

        image_stream = create_test_image(800, 200)  # very wide
        target_size = (120, 160)
        result = util.resize_image(image_stream, target_size)
        output = Image.open(BytesIO(result))
        assert output.size == target_size

    def test_tall_image_fits_within_target(self):
        """A tall image should be scaled to fit within the target dimensions."""
        import util

        image_stream = create_test_image(200, 800)  # very tall
        target_size = (120, 160)
        result = util.resize_image(image_stream, target_size)
        output = Image.open(BytesIO(result))
        assert output.size == target_size

    def test_small_image_is_not_scaled_up(self):
        """An image smaller than the target on both axes should not be enlarged."""
        import util

        image_stream = create_test_image(50, 50)  # smaller than target
        target_size = (120, 160)
        result = util.resize_image(image_stream, target_size)
        # Should still return bytes and produce output at the canvas size
        assert result is not None
        output = Image.open(BytesIO(result))
        assert output.size == target_size

    def test_exact_target_size_image(self):
        """An image that matches the target size exactly should be handled."""
        import util

        image_stream = create_test_image(120, 160)
        target_size = (120, 160)
        result = util.resize_image(image_stream, target_size)
        assert result is not None
        output = Image.open(BytesIO(result))
        assert output.size == target_size


# ---------------------------------------------------------------------------
# resize_image - EXIF orientation correction
# ---------------------------------------------------------------------------


class TestResizeImageExifOrientation:

    def _mock_exif(self, orientation_value):
        """Return a mock image whose _getexif returns the given orientation."""
        mock_image = MagicMock()
        mock_image.size = (200, 300)
        mock_image._getexif.return_value = {
            274: orientation_value
        }  # pylint: disable=protected-access
        mock_image.rotate.return_value = mock_image
        mock_image.resize.return_value = mock_image
        mock_image.mode = "RGB"
        return mock_image

    def test_no_exif_data_handled_silently(self):
        """Should continue processing when there is no EXIF data."""
        import util

        image_stream = create_test_image(200, 300)  # plain PNG, no EXIF
        result = util.resize_image(image_stream, (120, 160))
        assert result is not None

    def test_orientation_3_rotates_180(self):
        """Orientation 3 should rotate the image 180 degrees."""
        import util

        with patch("util.Image") as mock_pil:
            mock_image = self._mock_exif(3)
            final_image = MagicMock()
            final_image.size = (120, 160)
            mock_pil.open.return_value = mock_image
            mock_pil.new.return_value = final_image
            mock_pil.Resampling.LANCZOS = Image.Resampling.LANCZOS

            util.resize_image(BytesIO(b"fake"), (120, 160))
            mock_image.rotate.assert_called_with(180, expand=True)

    def test_orientation_6_rotates_270(self):
        """Orientation 6 should rotate the image 270 degrees."""
        import util

        with patch("util.Image") as mock_pil:
            mock_image = self._mock_exif(6)
            final_image = MagicMock()
            mock_pil.open.return_value = mock_image
            mock_pil.new.return_value = final_image
            mock_pil.Resampling.LANCZOS = Image.Resampling.LANCZOS

            util.resize_image(BytesIO(b"fake"), (120, 160))
            mock_image.rotate.assert_called_with(270, expand=True)

    def test_orientation_8_rotates_90(self):
        """Orientation 8 should rotate the image 90 degrees."""
        import util

        with patch("util.Image") as mock_pil:
            mock_image = self._mock_exif(8)
            final_image = MagicMock()
            mock_pil.open.return_value = mock_image
            mock_pil.new.return_value = final_image
            mock_pil.Resampling.LANCZOS = Image.Resampling.LANCZOS

            util.resize_image(BytesIO(b"fake"), (120, 160))
            mock_image.rotate.assert_called_with(90, expand=True)

    def test_exif_attribute_error_handled_silently(self):
        """Should continue if _getexif raises AttributeError (no EXIF at all)."""
        import util

        with patch("util.Image") as mock_pil:
            mock_image = MagicMock()
            mock_image.size = (200, 300)
            mock_image._getexif.side_effect = (
                AttributeError  # pylint: disable=protected-access
            )
            resized = MagicMock()
            resized.size = (120, 160)
            mock_image.resize.return_value = resized
            final_image = MagicMock()
            bytes_stream = BytesIO()
            Image.new("RGBA", (120, 160)).save(bytes_stream, "PNG")
            final_image.save = lambda s, fmt: s.write(bytes_stream.getvalue())
            mock_pil.open.return_value = mock_image
            mock_pil.new.return_value = final_image
            mock_pil.Resampling.LANCZOS = Image.Resampling.LANCZOS

            # Should not raise
            try:
                util.resize_image(BytesIO(b"fake"), (120, 160))
            except Exception as e:  # pylint: disable=broad-exception-caught
                pytest.fail(f"resize_image raised unexpectedly: {e}")


# ---------------------------------------------------------------------------
# resize_image - output format and mode
# ---------------------------------------------------------------------------


class TestResizeImageOutput:

    def test_output_is_rgba_mode(self):
        """Output PNG should be in RGBA mode (transparent canvas)."""
        import util

        image_stream = create_test_image(200, 200)
        result = util.resize_image(image_stream, (120, 160))
        output = Image.open(BytesIO(result))
        assert output.mode == "RGBA"

    def test_different_target_sizes(self):
        """Should work correctly for various target dimensions."""
        import util

        for size in [(100, 100), (200, 150), (50, 75)]:
            image_stream = create_test_image(300, 300)
            result = util.resize_image(image_stream, size)
            assert result is not None
            output = Image.open(BytesIO(result))
            assert output.size == size
