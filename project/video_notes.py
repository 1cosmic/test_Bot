

class Video_Notes():
    def __init__(self):
        self.question = {

            0: ["DQACAgIAAxkDAAIEzGRd8vhRTiQB0ki5rwABoyyTeacBTwACPSgAApAZ8UouYLgZLXp6MS8E"],
            1: ["DQACAgIAAxkDAAIEzWRd8wHTIzvkcAmuun5hkCfXOMtaAAI-KAACkBnxSl65FAABFce_pi8E"],
            2: ["DQACAgIAAxkDAAIEy2Rd8unrQhpOp_Dq3Qk1KF1mAAE3zQACPCgAApAZ8Upggca5gfdGIS8E"],
            3: ["DQACAgIAAxkDAAIEyWRd8tG_I8l4ItkjJWhF4Lj4a1hdAAI6KAACkBnxSs792xfNvOz4LwQ"],
            4: ["DQACAgIAAxkDAAIEuWRd8iiB8tf5tCTNxN5xhHLBGCeJAAIiKAACkBnxSruyaPYU3pDeLwQ",
                "DQACAgIAAxkDAAIEt2Rd8gUFCVIZGbF_-mC_esT1YcpMAAIgKAACkBnxSinw5V9uyZRwLwQ"],
            5: ["DQACAgIAAxkDAAIExGRd8pRYrEgH-Ztenf2pkhdJaC0-AAIwKAACkBnxStOnTI08CP77LwQ"],
            6: ["DQACAgIAAxkDAAIExWRd8p2SiCptWwKcx4FQ29PXThjVAAI0KAACkBnxSiLZNDrXprPCLwQ"],
            7: ["DQACAgIAAxkDAAIEyGRd8sHR_hRXcdZovhj58oEjponZAAI5KAACkBnxSjXrRWPRTEmILwQ"],
            8: ["DQACAgIAAxkDAAIEtmRd8f0kIAcpkF4DIXjwk_k6QJ9CAAIfKAACkBnxSjeISFKfAkI5LwQ"],
            9: ["DQACAgIAAxkDAAIEtWRd8eGLBvZFcGxTs-o8d3KkBYVZAAIeKAACkBnxSvtbvmSBCkLjLwQ"],
        }

        self.hint = {

            1: ["DQACAgIAAxkDAAIEsWRd7vJ0eYarn0SWMODZx6CNOlarAAIDKAACkBnxSrRrAonE-ZedLwQ",
                "DQACAgIAAxkDAAIEsGRd7u-qm-ZyA0TWpYnTQwE3wI2pAAICKAACkBnxSrjAgqxIktWvLwQ"],
            2: ["DQACAgIAAxkDAAIExmRd8qLuvRWQu-zuatJNA3fjJjzKAAI2KAACkBnxSpYpJa8Rm-_xLwQ"],
            3: ["DQACAgIAAxkDAAIEwWRd8nYe498K8Gbrlj676JXf91-vAAIrKAACkBnxSorqiUJvaqsULwQ",
                "DQACAgIAAxkDAAIEwGRd8nGSuQyDtNkqe0QYBuBdqJoSAAIqKAACkBnxSsVK_HLXe12CLwQ"],
            4: ["DQACAgIAAxkDAAIEzmRd8wpU7CnSHXowxnS2kysAAdwD7AACPygAApAZ8UoDEibTRdXfsi8E"],
            5: ["DQACAgIAAxkDAAIEw2Rd8oVHQ7TGMoB3rgtMCQABG2I4PwACLSgAApAZ8UqsEtUPKrf6My8E",
                "DQACAgIAAxkDAAIEwmRd8nwRri9kpT8SaXVyb0ZxNarBAAIsKAACkBnxSqhT6CurLJiXLwQ"],
            6: ["DQACAgIAAxkDAAIEvWRd8klerrxRIb80Wmf1Og75xYhmAAImKAACkBnxSun46tDt_Gm3LwQ",
                "DQACAgIAAxkDAAIEumRd8jLnkdxf0o2ERQ047KBzzzd5AAIjKAACkBnxSnRApVXCV8X-LwQ"],
            # 7: "",
            # 8: "",
            # 9: "",
            # 10: "",
        }

        self.dops = {

            "hello_start": "DQACAgIAAxkDAAIEu2Rd8jyaBu7eOhK1dENp75ySAlyjAAIkKAACkBnxSkj8XT-T0myOLwQ",
            "hello_go": "DQACAgIAAxkDAAIEvmRd8l2FMRZXSBhkIsAU5k9Jp_3AAAInKAACkBnxSh-WvcCAcvfjLwQ",
            "answer_true": ["DQACAgIAAxkDAAIEvGRd8kJrl0OADrsR7qA6x-SYqUQ2AAIlKAACkBnxSndCDR5ZzyvlLwQ",
                            "DQACAgIAAxkDAAIEv2Rd8muDw1rEfv_AlJhrSIp6IcwlAAIoKAACkBnxSqW0R1s8fRiTLwQ",
                            "DQACAgIAAxkDAAIEr2Rd7uw4xm61Y4yiGSJlZEyOFeIyAAIBKAACkBnxSqI5gLHDsm3uLwQ"],
            "goodbye": "DQACAgIAAxkDAAIEx2Rd8q1poMKHuZWFmFzUQcjsHoK9AAI3KAACkBnxSu_aG-RP8Lq8LwQ",
            "answer_false": ["DQACAgIAAxkDAAIEuGRd8gz128ZIYP_u8iYjwcAujTTVAAIhKAACkBnxSpxtEE_xO02cLwQ"],
            # 6: "",
            # 7: "",
            # 8: "",
            # 9: "",
            # 10: "",
        }