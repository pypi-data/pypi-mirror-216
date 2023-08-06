# downloads files from a URL, creates the same folder structure on the HDD as the URL has, and saves the file

## pip install requests2hdd

#### Tested against Windows 10 / Python 3.10 / Anaconda

### Simplified file downloading: 

This function simplifies the process of downloading a file from a URL and saving it to a local directory. You no longer need to write extensive code to handle these operations manually.

### Flexible status code handling: 

You can specify a collection of HTTP status codes that should be considered as successful downloads. By default, the function considers a status code of 200 as a successful download, but you can customize this based on your specific requirements. This allows you to define your own criteria for successful downloads.

### Preserves folder structure: 

The function automatically creates the same folder structure on the HDD as the URL has. It ensures that the downloaded file is saved in the appropriate folder according to its location in the URL. This feature helps maintain the organization and integrity of the downloaded files.

### Path correction on failure: 

If an exception occurs while saving the file, the function provides an option (correct_path_on_failure) to attempt to correct the file path. It utilizes the make_filepath_windows_comp function to replace illegal characters and resolve other path-related issues on Windows systems. This feature is especially useful when dealing with file paths that contain characters not supported by the operating system.

### Error handling: 

The function handles exceptions that occur during the file download and saving process. If correct_path_on_failure is set to False, the function raises the original exception, allowing you to handle errors according to your specific needs.

### Return value: 

Upon successful download and matching status code, the function returns the absolute path of the saved file. This provides you with the path information, which can be useful for further processing, verification, or referencing the downloaded file in your code.

```python

from requests2hdd import get_and_save

link = r'https://github.com/hansalemaos/screenshots/raw/main/neueswoerterbuch.txt'
path = 'c:\\downloadtest'
savepath = get_and_save(link,path,correct_path_on_failure=True)
print(savepath)

link = 'https://youtu.be/ZK9KzdqHVdE?t=12' # will substitute ? by _ on a Windows system 
path = 'c:\\downloadtest'
savepath = get_and_save(link,path,correct_path_on_failure=True)
print(savepath)

# output

c:\downloadtest\github.com\hansalemaos\screenshots\raw\main\neueswoerterbuch.txt
[Errno 22] Invalid argument: 'c:\\downloadtest\\youtu.be\\ZK9KzdqHVdE?t=12'
c:\downloadtest\youtu.be\ZK9KzdqHVdE_t=12


```