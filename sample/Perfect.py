import coverage

from sample.BucketList import bucket_list

cov = coverage.Coverage(branch=True)

cov.start()
bucket_list(1, 1, 1, 1, 1, 1)
bucket_list(2, 2, 2, 2, 2, 2)
bucket_list(4, 4, 4, 4, 4, 4)
bucket_list(8, 8, 8, 8, 8, 8)
bucket_list(16, 16, 16, 16, 16, 16)
bucket_list(32, 32, 32, 32, 32, 32)
bucket_list(64, 64, 64, 64, 64, 64)
bucket_list(128, 128, 128, 128, 128, 128)
bucket_list(256, 256, 256, 256, 256, 256)
bucket_list(512, 512, 512, 512, 512, 512)
bucket_list(1024, 1024, 1024, 1024, 1024, 1024)
bucket_list(2048, 2048, 2048, 2048, 2048, 2048)
# bucket_list(4096, 4096, 4096, 4096, 4096, 4096)
cov.stop()

data = cov.get_data()

filename = "D:\Spring 2023\\18668\Group Project\DataScience-T4\BucketList.py"

print(len(data.lines(filename)))
print(len(data.arcs(filename)))
