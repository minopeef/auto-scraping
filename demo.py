"""
This demo display the capabilities of Pymiere to batch some actions, without any human interactions.
It will start Premiere Pro, open a prproj file, pull data from it, make updates on it, save and close Premiere.
Before running this script make sure that you have a valid prproj path in the EXAMPLE_PRPROJ variable, the prproj should
contain at least sequence named 'hello world'. Also make sure no instance of Premiere Pro are running.
"""
import os
import time

import pymiere

# EXAMPLE_PRPROJ = r"default.prproj"  # replace by your own prproj

# if not os.path.isfile(EXAMPLE_PRPROJ):
#     raise ValueError("Example prproj path does not exists on disk '{}'".format(EXAMPLE_PRPROJ))

# # start premiere
# print("Starting Premiere Pro...")
# if pymiere_exe.is_premiere_running()[0]:
#     raise ValueError("There already is a running instance of premiere")
# pymiere_exe.start_premiere()

# # open a project
# print("Opening project '{}'".format(EXAMPLE_PRPROJ))
# error = None
# # here we have to try multiple times, as on slower systems there is a slight delay between Premiere initialization
# # and when the PymiereLink panel is started and ready to receive commands. Most install will succeed on the first loop
# for x in range(20):
#     try:
#         pymiere.objects.app.openDocument(EXAMPLE_PRPROJ)
#     except Exception as error:
#         time.sleep(0.5)
#     else:
#         break
# else:
#     raise error or ValueError("Couldn't open path '{}'".format(EXAMPLE_PRPROJ))

os.popen("target.prproj")

for x in range(20):
    try:
        assert pymiere.objects.app.isDocumentOpen(), "loading"
    except:  # noqa
        time.sleep(1)

# set sequence named hello world as active sequence
print("Opening sequence named 'hello world'")
sequences = pymiere.objects.app.project.sequences
sequence = [s for s in sequences if s.name == "hello world"]  # search sequence by name
if not sequence:
    raise NameError("This demo only work if a sequence is named 'hello world")
sequence = sequence[0]
pymiere.objects.app.project.openSequence(sequence.sequenceID)
pymiere.objects.app.project.activeSequence = sequence

# rename sequence and display info
print(f"Renaming active sequence '{pymiere.objects.app.project.activeSequence.name}'")
pymiere.objects.app.project.activeSequence.name = "renamed sequence"
print(
    f"Sequence has been renamed to '{pymiere.objects.app.project.activeSequence.name}'"
)
print(
    f"Current timeline player time is '{pymiere.objects.app.project.activeSequence.getPlayerPosition().seconds}'"
)
pymiere.objects.app.project.activeSequence.name = (
    "hello world"  # rename back for test to work next time
)

# import files
print("importing files")
pymiere.objects.app.project.importFiles(
    ["C:\\Users\\admin\\Documents\\project\\auto-scraping\\test.png"],
    True,
    pymiere.objects.app.project.rootItem,
    True,
)

# var importSingleFile = File.openDialog ("Import Video File");
# var importAry = [];
# importAry.push(importSingleFile.fsName);
# app.project.importFiles(importAry);
# close premiere
print("Now closing")
pymiere.objects.app.project.saveAs("savetest.prproj")
try:
    pymiere.objects.app.quit()
except Exception as e:
    print(e)
print("Successfully batched some actions in Premiere Pro")
