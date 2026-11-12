import unittest

from jobs import generation_prompt


class WorkflowPromptTests(unittest.TestCase):
    def test_image_guidance_keeps_upstream_wording_and_user_language(self):
        prompt = "把人物替换成参考角色，保持原有动作。"
        expected = prompt + (
            "\n@Video1 contains the colored-depth composite and embedded isolated vocals pitched up three semitones, "
            "without the music bed; use its embedded audio for performance and lip synchronization. "
            "@Image1 is the only replacement character reference."
        )
        self.assertEqual(
            generation_prompt(prompt, identity_video=False, second_reference=False, mode="depth"),
            expected,
        )

    def test_video_identity_guidance_uses_original_appearance_only_instruction(self):
        prompt = "Use this character."
        expected = prompt + (
            "\n@Video1 is the source edit and contains isolated vocals pitched +3 semitones. "
            "@Video2 is only the primary character visual identity reference. Use only @Video1 audio for speech timing."
        )
        self.assertEqual(
            generation_prompt(prompt, identity_video=True, second_reference=False, mode="depth"),
            expected,
        )

    def test_mesh_modes_keep_audio_mapping_reference_mapping_and_removal_instruction(self):
        for mode, description in (
            ("face_mesh", "original video with face mesh overlay"),
            ("depth_mesh", "depth composite with face mesh overlay"),
        ):
            with self.subTest(mode=mode):
                result = generation_prompt(
                    "Match @Audio1.", identity_video=False, second_reference=True, mode=mode,
                )
                expected = (
                    "Match the audio embedded in @Video1."
                    f"\n@Video1 contains the {description} and embedded isolated vocals pitched up three semitones, "
                    "without the music bed; use its embedded audio for performance and lip synchronization. "
                    "@Image1 is the primary character reference; @Image2 is the secondary character reference."
                    " Remove all face mesh lines and any depth colors from the output; use them only for expression and lip motion guidance. "
                    "Replace the entire original identity including hair. Preserve the exact embedded dialogue and timing."
                )
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
