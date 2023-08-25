import os

name = "MarryBye"
version = "1.20.1"
gameDir = "./"
minecraft_jar = os.path.join(
    ".\\", "versions", "gmrs-forge-1.20.1", "gmrs-forge-1.20.1.jar")
main_class = "net.minecraft.client.main.Main"


libs = os.path.join(
    ".\\", "libraries")
lib_files = []

for adress, dir, files in os.walk(libs):
    for file in files:
        lib_files.append(os.path.join(adress, file))

class_path = ""
for file in lib_files:
    class_path += file + ";"

java_args = f"-server -splash:splash.png -d64 -da -dsa -Xrs -Xms2048M -Xmx2048M -XX:NewSize=2048M -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode -XX:-UseAdaptiveSizePolicy -XX:+DisableExplicitGC -Djava.library.path={libs} -cp {class_path} {main_class}"

os.system(
    f"java {java_args} --username {name} --version {version} --gameDir {gameDir}")
