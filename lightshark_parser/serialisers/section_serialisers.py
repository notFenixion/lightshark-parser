
def serialise_lightshow(lightshow: Lightshow) -> bytes:
    file_bytes = bytearray()

    if lightshow.fileinfo:
        file_bytes.extend(serialise_fileinfo(lightshow.fileinfo))


    return file_bytes


def serialise_fileinfo(fileinfo: FileInfo) -> bytes:

    file_bytes = bytearray()
    file_bytes.extend(section_header("#fileinfo#"))
    

    ## Version ##

        
    
    return