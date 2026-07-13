from __future__ import annotations

import importlib.util
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Union


def _find_ffmpeg() -> str:
    """Returnerar sökväg till ffmpeg-binären, eller kastar ett tydligt fel."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg

    # Fallback: imageio-ffmpeg (kan ge en ffmpeg-binär via Python).
    # Kontrollera först att paketet finns så importen inte behöver ligga i ett
    # generellt try/except-block.
    if importlib.util.find_spec("imageio_ffmpeg") is not None:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()

    raise RuntimeError(
        "Hittade ingen ffmpeg.\n\n"
        "Lösning A (rekommenderad): installera ffmpeg och lägg i PATH.\n"
        "  - Linux: sudo apt install ffmpeg\n"
        "  - macOS: brew install ffmpeg\n"
        "  - Windows: installera ffmpeg och lägg till i PATH\n\n"
        "Lösning B: pip install imageio-ffmpeg\n"
    )


def audio_bild_till_mp4(
    ljudfil: Union[str, Path],
    bildfil: Union[str, Path],
    utfil: Union[str, Path],
    *,
    fps: int = 30,
    upplosning: Optional[Tuple[int, int]] = (1920, 1080),
    ljud_bitrate: str = "192k",
    overwrite: bool = True,
) -> Path:
    """
    Slår ihop en ljudfil + stillbild till en MP4.
    Bilden visas hela ljudets längd.

    Parametrar:
      - ljudfil: t.ex. "voice.mp3" / "audio.wav"
      - bildfil: t.ex. "cover.jpg" / "still.png"
      - utfil:   t.ex. "result.mp4"
      - fps: videons framerate (30 standard)
      - upplosning: (bredd, höjd) eller None för att behålla bildens storlek
      - ljud_bitrate: t.ex. "192k"
      - overwrite: skriv över om utfil redan finns

    Returnerar:
      Path till skapad mp4.
    """
    ffmpeg = _find_ffmpeg()

    ljudfil = Path(ljudfil)
    bildfil = Path(bildfil)
    utfil = Path(utfil)

    if not ljudfil.is_file():
        raise FileNotFoundError(f"Ljudfil saknas: {ljudfil}")
    if not bildfil.is_file():
        raise FileNotFoundError(f"Bildfil saknas: {bildfil}")

    utfil.parent.mkdir(parents=True, exist_ok=True)

    # Video-filter: skala/padda till vald upplösning (om angiven),
    # samt säkra kompatibelt pixel-format och jämna dimensioner för H.264.
    vf_parts = []
    if upplosning is not None:
        w, h = upplosning
        vf_parts += [
            f"scale={w}:{h}:force_original_aspect_ratio=decrease",
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2",
        ]
    vf_parts += [
        "format=yuv420p",
        "scale=trunc(iw/2)*2:trunc(ih/2)*2",
    ]
    vf = ",".join(vf_parts)

    cmd = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        ("-y" if overwrite else "-n"),
        "-loop",
        "1",
        "-framerate",
        str(fps),
        "-i",
        str(bildfil),
        "-i",
        str(ljudfil),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-c:a",
        "aac",
        "-b:a",
        ljud_bitrate,
        "-shortest",
        "-movflags",
        "+faststart",
        str(utfil),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        msg = stderr or stdout or str(exc)
        raise RuntimeError(f"ffmpeg misslyckades:\n{msg}") from exc

    return utfil


# Exempel:
# audio_bild_till_mp4("ljud.mp3", "bild.jpg", "klar.mp4", upplosning=(1280, 720))
