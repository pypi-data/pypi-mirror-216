import ffmpeg
import pyass


def convert_to_ass(input_srt_file, output_ass_file):
    ffmpeg.input(input_srt_file).output(
        output_ass_file, format="ass"
    ).overwrite_output().run()


def change_style(input_srt_file, output_ass_file, style):
    tmp_ass_file = "/tmp/tmp.ass"
    convert_to_ass(input_srt_file, tmp_ass_file)

    new_style = pyass.Style()

    for key, value in style.items():
        setattr(new_style, key, value)

    with open(tmp_ass_file, encoding="utf_8_sig") as f:
        script = pyass.load(f)

    script.styles[0] = new_style
    with open(output_ass_file, "w", encoding="utf_8_sig") as f:
        pyass.dump(script, f)


def set_script_info(filename, w, h):
    with open(filename, encoding="utf_8_sig") as f:
        script = pyass.load(f)

    script.scriptInfo = pyass.ScriptInfoSection(
        [
            ("ScriptType", "v4.00+"),
            ("PlayResX", f"{w}"),
            ("PlayResY", f"{h}"),
            ("ScaledBorderAndShadow", "yes"),
            ("YCbCr Matrix", "None"),
        ]
    )
    with open(filename, "w", encoding="utf_8_sig") as f:
        pyass.dump(script, f)
