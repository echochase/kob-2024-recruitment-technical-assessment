from dataclasses import dataclass
from collections import defaultdict
# the collections library should come pre-installed to Python as it's standard library

@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int

# Helper function
def idToFile(id: int, files: list[File]) -> File:
    for file in files:
        if file.id == id:
            return file

"""
Task 1
"""
# Didn't really wanna do a tree-like structure so I came up with this
# it's a bit unorthodox but shouldn't be too slow
def leafFiles(files: list[File]) -> list[str]:
    temp = defaultdict(int)
    for file in files:
        # To register that a 'candidate' leaf file by adding its ID
        temp[str(file.id)] += 1
        # If someone has a parent, 'remove' it from the register.
        # doesn't matter if it's already removed; we'll just see
        # which keys in temp have a positive value in them
        if file.parent >= 0:
            temp[str(file.parent)] -= 1
    # Yea I know it's spelt 'leaves' but it just seems wrong since I'm referring to leaf files
    leafs = []
    for key, value in temp.items():
        # If no-one has registered this ID as a parent
        if value == 1:
            leafs.append(idToFile(int(key), files).name)
    return leafs


"""
Task 2
"""
def kLargestCategories(files: list[File], k: int) -> list[str]:
    categories = defaultdict(int)
    # Register a file's categories
    for f in files:
        for c in f.categories:
            categories[c] += 1
    i = 0
    result = []
    # think of each key-value pair in *categories* as a tuple
    # we sort by categories[name] (which is size) first, desendingly,
    # then by name, ascendingly
    for category in sorted(categories.keys(), key=lambda name: (-categories[name], name)):
        if i < k:
            i += 1
            result.append(category)
    return result

"""
Task 3
"""
def largestFileSize(files: list[File]) -> int:
    if not files:
        return 0
    fileSizes = defaultdict(int)
    # Register the file's own size
    for file in files:
        fileSizes[str(file.id)] += file.size
        recurse = file
        # If it has parents, so long as the chain goes up,
        # add to their size.
        while recurse.parent != -1:
            fileSizes[str(recurse.parent)] += file.size
            recurse = idToFile(recurse.parent, files)
    return max(fileSizes.values())


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]

    assert largestFileSize(testFiles) == 20992

# More tests (hey look im boundary checking)
    
    # Root folder dominates
    testFiles2 = [
        File(3, "Folder", ["Folder"], -1, 0),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(2, "Folder3", ["Folder"], 34, 0),
        File(1, "Folder4", ["Folder"], 2, 0),
        File(10, "audio.mp3", ["Media"], 34, 300),
        File(20, "baudio.mp3", ["Media"], 1, 20),
        File(35, "name.txt", ["Documents"], 3, 1024)
    ]

    # Big fat file dominates
    testFiles3 = [
        File(3, "Folder", ["Folder"], -1, 0),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(2, "Folder3", ["Folder"], 34, 0),
        File(1, "Folder4", ["Folder"], 2, 0),
        File(10, "audio.mp3", ["Media"], 34, 300),
        File(20, "baudio.mp3", ["Media"], 1, 20),
        File(35, "name.txt", ["Documents"], 3, 1024),
        File(121, "big ass file", ["Documents"], -1, 10240)
    ]

    # Another structure
    assert sorted(leafFiles(testFiles3)) == [
        "audio.mp3",
        "baudio.mp3",
        "big ass file",
        "name.txt"
    ]

    # Full List
    assert kLargestCategories(testFiles, 10) == [
        "Documents", "Folder", "Media", "Excel", "Audio", "Backup",
        "Photos", "Presentation", "Programming", "Videos"
    ]

    # Out of bounds
    assert kLargestCategories(testFiles, 200) == [
        "Documents", "Folder", "Media", "Excel", "Audio", "Backup",
        "Photos", "Presentation", "Programming", "Videos"
    ]
    
    # Single
    assert kLargestCategories(testFiles, 1) == ["Documents"]

    # None
    assert kLargestCategories(testFiles, 0) == []

    # Root should be biggest
    assert largestFileSize(testFiles2) == 1344

    # Biggest file not part of root
    assert largestFileSize(testFiles3) == 10240