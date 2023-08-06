import argparse
import sys
import cv2
import csv
import time
from pupil_detectors import Detector2D

detector = Detector2D()


# This function is to display progressive bar
def print_percent_done(index_input, total, bar_len=50, title_input='Please wait'):
    percent_done = (index_input + 1) / total * 100
    percent_done_round = round(percent_done, 1)

    done = int(round(percent_done_round / (100 / bar_len)))
    togo = bar_len - done

    done_str = '█' * done
    togo_str = '░' * togo

    sys.stdout.write(f'\r{title_input}: [{done_str}{togo_str}] {percent_done_round}% done')


# This function is to change from frame count to frame time to be used as pupil time
def frame_to_time(frame_number, frame_rate):
    return frame_number / frame_rate


def main():
    parser = argparse.ArgumentParser(prog='vgetpupil',
                                     description='VGETPUPIL package.')
    parser.add_argument('--version', action='version', version='1.0.4'),
    parser.add_argument("-i", dest="input_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="input mp4 file", metavar="filename.mp4")
    parser.add_argument("-o", dest="output_filename", required=True, type=argparse.FileType('w'), default=sys.stdout,
                        help="output csv file", metavar="filename.csv")
    parser.add_argument("-e", dest="eye_id_input", required=False, type=int, default=None, help="eye id input",
                        metavar="0 or 1")

    args = parser.parse_args()
    input_file = args.input_filename.name
    output_file = args.output_filename.name
    eye_id_input_from_user = args.eye_id_input
    eye_side_input = None
    convert_able = True

    # Define conditions to decide input mp4 is left or right eye video
    left_eye_indicated_string = "left" in str(input_file).lower() or "0" in str(input_file).lower()
    right_eye_indicated_string = "right" in str(input_file).lower() or "1" in str(input_file).lower()

    # Handle error for type of input file
    if str(input_file).endswith(".mp4"):
        if eye_id_input_from_user == 0 or eye_id_input_from_user == 1:
            eye_side_input = eye_id_input_from_user

            # Handle warning when the force eye id input is opposite with the file name
            if eye_id_input_from_user == 1 and left_eye_indicated_string:
                print("Warning! Eye id input is not compatible with input file name.")
                print(f"Eye id input is {eye_id_input_from_user}.")
                print(f"Input file name is {input_file}.")

            # Handle warning when the force eye id input is opposite with the file name
            if eye_id_input_from_user == 0 and right_eye_indicated_string:
                print("Warning! Eye id input is not compatible with input file name.")
                print(f"Eye id input is {eye_id_input_from_user}.")
                print(f"Input file name is {input_file}.")

        # Handle error of invalid input when force eye id input is not 0 and 1
        elif eye_id_input_from_user is not None and (eye_id_input_from_user > 1 or eye_id_input_from_user < 0):
            print("Invalid eye id put! It must be 0 or 1.")
            convert_able = False

        # Handle when there is no force eye id input
        elif eye_id_input_from_user is None:
            if left_eye_indicated_string:
                eye_side_input = 0
            elif right_eye_indicated_string:
                eye_side_input = 1
            else:
                print("The input file name must contains \"left\" or \"right\" or \"0\" or \"1\".")
                print("                               (or)")
                print("We can force eye id input as \"-e 0 or -e 1\"")
                convert_able = False
    else:
        convert_able = False
        print("Input file must be mp4.")

    # Handle error when the output file name is not csv
    if str(output_file).endswith(".csv"):
        pass
    else:
        convert_able = False
        print("Output file must be csv.")

    if convert_able:
        print("Input file name:", input_file)
        print("Output file name:", output_file)
        input_video = cv2.VideoCapture(input_file)
        frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("Input frame width:", frame_width)
        frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Input frame height:", frame_height)
        frame_rate = input_video.get(cv2.CAP_PROP_FPS)
        print("Input frame rate:", frame_rate)
        frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Input frame count:", frame_count)

        # Open the output file to write the data
        with open(output_file, mode='w', newline="") as destination_file:
            header_names = ["pupil_time", "eye_id", "confidence", "norm_pos_x",
                            "norm_pos_y", "diameter", "ellipse_center_x", "ellipse_center_y",
                            "ellipse_axis_a", "ellipse_axis_b", "ellipse_angle"]
            csv_writer = csv.DictWriter(destination_file, fieldnames=header_names)
            csv_writer.writeheader()

            w_start = time.time()
            count = 0

            while True:
                # r_start = time.time()
                ret, frame = input_video.read()
                print_percent_done(count, frame_count)
                # r_stop = time.time()
                # print(f"read time {(r_stop - r_start) * 1000}")

                # When there is frame to read
                if ret:
                    pupil_time = frame_to_time(count, frame_rate)
                    count += 1
                    cur_time = time.time()
                    # print(pupil_time)
                    # print(type(frame))
                    eye_id = eye_side_input
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # d_start = time.time()
                    result = detector.detect(gray)
                    # d_stop = time.time()
                    # print(f"detecter time {(d_stop - d_start) * 1000} milisec")
                    confidence = result["confidence"]
                    ellipse = result["ellipse"]
                    ellipse_center_x = ellipse["center"][0]
                    ellipse_center_y = ellipse["center"][1]
                    ellipse_axis_a = ellipse["axes"][0]
                    ellipse_axis_b = ellipse["axes"][0]
                    ellipse_angle = ellipse["angle"]
                    diameter = result["diameter"]
                    x_nom = ellipse_center_x / 192
                    y_nom = ellipse_center_y / 192
                    csv_writer.writerow({"pupil_time": pupil_time,
                                         "eye_id": eye_id,
                                         "confidence": confidence,
                                         "norm_pos_x": x_nom,
                                         "norm_pos_y": y_nom,
                                         "diameter": diameter,
                                         "ellipse_center_x": ellipse_center_x,
                                         "ellipse_center_y": ellipse_center_y,
                                         "ellipse_axis_a": ellipse_axis_a,
                                         "ellipse_axis_b": ellipse_axis_b,
                                         "ellipse_angle": ellipse_angle, })
                    # print(f"process time {(time.time() - cur_time) * 1000}")
                    # print(f"one loop time {(time.time() - r_start) * 1000}")

                # When there is no frame to read
                else:
                    input_video.release()
                    cv2.destroyAllWindows()
                    destination_file.close()
                    break

        # w_stop = time.time()
        # print(f"whole time {(w_stop - w_start) / 60}")
