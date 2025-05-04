bl_info = {
    "name": "Multi-Audio Track Video Importer",
    "author": "Parham Ettehadieh",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Video Sequence Editor > Sidebar > Multi-Audio",
    "description": "Import video with selectable audio tracks using FFmpeg",
    "category": "Sequencer",
    "warning": "This add-on was created with the help of AI.",
    "doc_url": "https://www.youtube.com/@macarthurz",
}

import bpy
import subprocess
import os
import tempfile
import json
from bpy.props import StringProperty, CollectionProperty, BoolProperty, IntProperty
from bpy.types import Operator, Panel, PropertyGroup, UIList

# Helper: call ffprobe to get audio track info
def get_audio_tracks(video_path):
    try:
        result = subprocess.run([ 
            "ffprobe", "-v", "error", "-select_streams", "a", 
            "-show_entries", "stream=index:stream_tags=language", 
            "-of", "json", video_path 
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("ffprobe failed:", result.stderr)
            return None

        data = json.loads(result.stdout)
        return data.get("streams", [])

    except Exception as e:
        print("Error running ffprobe:", e)
        return None

# Property group for each audio track
class AudioTrackItem(PropertyGroup):
    index: StringProperty(name="Index")
    language: StringProperty(name="Language")
    selected: BoolProperty(name="Import", default=False)

# UI list for showing audio tracks
class AUDIO_UL_TrackList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, "selected", text="")
        row.label(text=f"Track {item.index}")
        row.label(text=item.language or "unknown")

# UI panel in the Video Sequence Editor
class SEQUENCER_PT_MultiAudioImport(Panel):
    bl_label = "Multi-Audio Import"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Multi-Audio'

    def draw(self, context):
        layout = self.layout
        props = context.scene.multi_audio_props

        layout.prop(props, "video_path")
        layout.operator("multi_audio.scan_tracks", icon="FILE_REFRESH")

        if props.tracks:
            layout.template_list("AUDIO_UL_TrackList", "", props, "tracks", props, "track_index")
            layout.operator("multi_audio.import_video", icon="SEQ_SEQUENCER")

# Operator: scan for audio tracks
class AUDIO_OT_ScanTracks(Operator):
    bl_idname = "multi_audio.scan_tracks"
    bl_label = "Scan Audio Tracks"

    def execute(self, context):
        props = context.scene.multi_audio_props
        props.tracks.clear()

        video_path = bpy.path.abspath(props.video_path)

        if not os.path.isfile(video_path):
            self.report({'ERROR'}, "Invalid video file path.")
            return {'CANCELLED'}

        tracks = get_audio_tracks(video_path)

        if tracks is None:
            self.report({'ERROR'}, "Failed to read audio tracks using ffprobe.")
            return {'CANCELLED'}

        if not tracks:
            self.report({'WARNING'}, "No audio tracks found.")
            return {'CANCELLED'}

        # Add audio tracks with fallback for missing language tags
        for i, t in enumerate(tracks):
            item = props.tracks.add()
            item.index = str(t.get("index", i))
            tags = t.get("tags", {})
            item.language = tags.get("language", f"Track {i + 1}")

        self.report({'INFO'}, f"Found {len(props.tracks)} audio track(s).")
        return {'FINISHED'}

# Operator: import video and selected audio
class AUDIO_OT_ImportVideo(Operator):
    bl_idname = "multi_audio.import_video"
    bl_label = "Import Video and Selected Audio"

    def execute(self, context):
        props = context.scene.multi_audio_props
        video_path = bpy.path.abspath(props.video_path)

        if not os.path.isfile(video_path):
            self.report({'ERROR'}, "Video file path is invalid.")
            return {'CANCELLED'}

        # Create sequence editor if it doesn't exist
        if not context.scene.sequence_editor:
            context.scene.sequence_editor_create()

        # Import video
        try:
            bpy.ops.sequencer.movie_strip_add(filepath=video_path, frame_start=1)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to add video: {e}")
            return {'CANCELLED'}

        # Import selected audio tracks
        for t in props.tracks:
            if t.selected:
                temp_path = os.path.join(tempfile.gettempdir(), f"audio_track_{t.index}.wav")
                try:
                    subprocess.run([
                        "ffmpeg", "-y", "-i", video_path,
                        "-map", f"0:a:{t.index}", "-vn", temp_path
                    ], capture_output=True, text=True)

                    bpy.ops.sequencer.sound_strip_add(filepath=temp_path, frame_start=1)

                except Exception as e:
                    self.report({'ERROR'}, f"Failed to import audio track {t.index}: {e}")
                    continue

        self.report({'INFO'}, "Import completed.")
        return {'FINISHED'}

# Property container
class MultiAudioProperties(PropertyGroup):
    video_path: StringProperty(
        name="Video File",
        subtype='FILE_PATH'
    )
    tracks: CollectionProperty(type=AudioTrackItem)
    track_index: IntProperty()

# Register/unregister
classes = (
    AudioTrackItem,
    AUDIO_UL_TrackList,
    SEQUENCER_PT_MultiAudioImport,
    AUDIO_OT_ScanTracks,
    AUDIO_OT_ImportVideo,
    MultiAudioProperties,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.multi_audio_props = bpy.props.PointerProperty(type=MultiAudioProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.multi_audio_props

if __name__ == "__main__":
    register()
