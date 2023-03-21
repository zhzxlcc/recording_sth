rs_txt = defaultdict(list) 
rs_list = []
with open(text_frames_scoring_file) as f:
    for line in f:
        j = json.loads(line.strip())
        video_name = download_object(url=j['video_url'])  # 返回包括路径的video name
        # print(video_name)
        img_names = capture_pic(video_name=video_name)
        if os.path.exists(video_name):
            os.remove(video_path)  # 删除视频
        else:
            print('no such file: %s' % video_name)
        rs_txt['score'] = j['score']
        # rs_txt["frames"] = img_names
        rs_txt["frames"] = [x.replace("a", "b") for x in img_names]
        rs_list.append(copy.deepcopy(rs_txt))
    # print(len(rs_list),rs_list)

with open(f'./frames_scoring_own.txt', 'w+') as f:
    for i in range(len(rs_list)):
       f.write(f'{json.dumps(rs_list[i], ensure_ascii=False)}\n') #按行写入，json写入单个字典
