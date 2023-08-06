from biliup.plugins.bili_webup import BiliBili, Data


path = 'videos/336253631876_20230626_223838.mp4'

file_list = [path]


video = Data()
video.title = path
video.desc = 'test'
video.source = 'showroom'
video.tid = 137
video.set_tag(['showroom'])
video.dynamic = 'showroom test'
video.copyright = 2
lines = 'AUTO'
tasks = 3
dtime = 0

with BiliBili(video) as bili:
    bili.login("bili.cookie", {
        'cookies':{
            'SESSDATA': 'ce166d20%2C1703133051%2Cbfd8e562',
            'bili_jct': '36903df9cfed8b7c71db080dd1d7793f',
            'DedeUserID__ckMd5': '5ac189ef818fb725',
            'DedeUserID': '12814697'
        },'access_token': '4ee89ad2f670c7536ba029efe2f84062'})
    # bili.login_by_password("username", "password")
    for file in file_list:
        video_part = bili.upload_file(file, lines=lines, tasks=tasks)
        video.append(video_part)
    video.delay_time(dtime)
    ret = bili.submit()