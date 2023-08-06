# 计算机登录用户: jk
# 系统日期: 2023/5/25 14:22
# 项目名称: chipeak_cv_data_tool
# 开发者: zhanyong
import os
import cv2

"""
单个视频文件处理实现类
"""


class Split(object):
    @classmethod
    def video_cut_images_loader(cls, q, video_path, interval, images_dir, labelme_dir, filename_format):
        """
        提取视频帧图片并保存
        :param q: 进程池队列，每一个视频文件当作一个进程，进行提取
        :param video_path: 视频路径
        :param interval: 帧提取频率
        :param images_dir:图片保存保存路径
        :param labelme_dir:json文件保存路径
        :param filename_format:文件格式
        """
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labelme_dir, exist_ok=True)
        video = cv2.VideoCapture(video_path)
        cur_frame = 0
        num = 1
        while True:
            ret, frame = video.read()
            if not ret:
                break
            if cur_frame % int(interval) == 0:
                image_name = filename_format.format(cur_frame)
                img_dir = os.path.join(images_dir, image_name)
                cv2.imencode('.jpg', frame)[1].tofile(img_dir)
                num += 1
            cur_frame += 1
        # 如果提取视频帧完成，那么就向队列中写入一个消息，表示已经完成
        q.put(video_path)

    @classmethod
    def video_time_cut_loader(cls, q, video_path, save_path, start_time, end_time, height, weight):
        """
        按时间截取视频文件
        :param q: 进程池队列，每一个视频文件当作一个进程，进行提取
        :param video_path: 视频路径
        :param save_path: 视频保存路径
        :param start_time: 视频截取开始时间以秒为单位
        :param end_time: 视频截取结束时间以秒为单位
        :param height: 保存视频的高度
        :param weight: 保存视频的宽度
        """
        # mkdir_save_path = os.path.dirname(save_path)
        os.makedirs(save_path, exist_ok=True)
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(video_path, fourcc, fps, (weight, height), True)
        connt = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break
            else:
                connt += 1
                if (connt > (start_time * fps)) and connt <= (end_time * fps):
                    img_copy = cv2.resize(frame, (weight, height), interpolation=cv2.INTER_CUBIC)
                    writer.write(img_copy)
                if (connt == (end_time * fps)):
                    break
        writer.release()
        # 如果提取视频帧完成，那么就向队列中写入一个消息，表示已经完成
        q.put(video_path)

    @classmethod
    def video_fps_cut_loader(cls, q, video_path, save_path, cut_frame_length):
        """
        按帧号截取视频文件
        @param q: 进程池队列，每一个视频文件当作一个进程，进行提取
        @param video_path: 输入视频路径
        @param save_path: 输出视频路径
        @param cut_frame_length: 帧号数量
        """
        mkdir_save_path = os.path.dirname(save_path)
        os.makedirs(mkdir_save_path, exist_ok=True)
        video_capture = cv2.VideoCapture(video_path)
        fps = video_capture.get(5)
        print(video_capture.isOpened())
        print("fps", video_capture.get(5))
        print("COUNT", video_capture.get(7))
        size = (int(video_capture.get(3)), int(video_capture.get(4)))
        frame_index = 0
        flag = 0
        success, bgr_image = video_capture.read()
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        final_path = os.path.join(save_path, str(frame_index // cut_frame_length) + '.mp4')
        print(final_path)
        v = cv2.VideoWriter(final_path, fourcc, fps, size)
        while success:
            if v.isOpened():
                v.write(bgr_image)
            if frame_index == cut_frame_length * flag + cut_frame_length:
                if v.isOpened():
                    v.release()
            if frame_index == cut_frame_length * flag:
                final_path = os.path.join(save_path, str(frame_index // cut_frame_length) + '.mp4')
                v = cv2.VideoWriter(final_path, fourcc, fps, size)
                flag += 1
            success, bgr_image = video_capture.read()
            frame_index = frame_index + 1
        video_capture.release()  # 关闭打开视频流
        v.release()  # 关闭打开视频流
        # 如果提取视频帧完成，那么就向队列中写入一个消息，表示已经完成
        q.put(video_path)
