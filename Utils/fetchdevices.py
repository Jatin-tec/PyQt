# Read video URLs from a .txt file
def read_video_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        video_urls = [line.strip() for line in lines]
    file.close()    
    return video_urls