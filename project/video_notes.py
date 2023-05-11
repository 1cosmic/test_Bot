

class Video_Notes():
    def __init__(self):
        self.question = {

            0: ["DQACAgIAAxkDAAMhZFz0i9gIbzoyDD2Sg1lhUKnuk0wAAuwwAAJRyulK0ugW7h74K90vBA"],
            1: ["DQACAgIAAxkDAAMiZFz0pNLNT6w_lyDKBUUZXk8c1XMAAu4wAAJRyulK1fhidrfW27cvBA"],
            2: ["DQACAgIAAxkDAAMgZFz0gvSZRweSQpg3HXCQYcZEHV8AAuowAAJRyulK8Hf9jCxhjIQvBA"],
            3: ["DQACAgIAAxkDAAMeZFz0e2hrOsCnOa9XhIZSAp678LcAAugwAAJRyulK3SjclmzIzfovBA"],
            4: ["DQACAgIAAxkDAAMOZFzzpBZMjbIcSvghfOWSHB13gDAAAtMwAAJRyulKvbzdr1Ly-0gvBA",
                "DQACAgIAAxkDAAMMZFzzm4TrQMj_SII0lfjCRATHSBoAAtEwAAJRyulK_wrmQy157BsvBA"],
            5: ["DQACAgIAAxkDAAMZZFz0CZncd2j5Cb0h0zcsbb7pSmgAAuIwAAJRyulK3JnfgGBvvcYvBA"],
            6: ["DQACAgIAAxkDAAMaZFz0HNRitEihyKPG2sLpwf5Vvp0AAuQwAAJRyulKo7PAzpLSylUvBA"],
            7: ["DQACAgIAAxkDAAMdZFz0dzGKkBCsoRLR8w_NlyKvgSsAAucwAAJRyulKA5N8tMqx9QIvBA"],
            8: ["DQACAgIAAxkDAAMLZFzzkVprJuhFQw0iyCwX3xmSNqwAAtAwAAJRyulKnsnVa-WbrCkvBA"],
            9: ["DQACAgIAAxkDAAMKZFzzha75590MgNTc_y19YgvQPQMAAs8wAAJRyulK2oQ6O8MlHuMvBA"],
        }

        self.hint = {

            1: ["DQACAgIAAxkDAAMJZFzzURuuxnA9vdPWhRiPR3jKJjQAAs0wAAJRyulKvIBHeyY9sV4vBA",
                "DQACAgIAAxkDAAMIZFzzTdm4jFyv4zCTRn2LZ-XcG4EAAsswAAJRyulK9XxIoc6FKewvBA"],
            2: ["DQACAgIAAxkDAAMbZFz0L1jnVeEoKTinpabVkY1JJ7AAAuUwAAJRyulKL8tCCuOb0IwvBA"],
            3: ["DQACAgIAAxkDAAMWZFzz1GdYZjJ6aITMOuvT43ypMdkAAt0wAAJRyulKOfCQkCpL6cEvBA",
                "DQACAgIAAxkDAAMVZFzzyZsDLCM24xLwN1OHex31EckAAtswAAJRyulKUTOXMz7_QQcvBA"],
            4: ["DQACAgIAAxkDAAMjZFz0rOy-TmOSxdrJaWY1En0XaPwAAu8wAAJRyulK6exeTwSuHOQvBA"],
            5: ["DQACAgIAAxkDAAMYZFzz8pa2OdIvIuxzQ8sSCVsrPHYAAuEwAAJRyulKdieSTtlhuRYvBA",
                "DQACAgIAAxkDAAMXZFzz5Kqjk1rCLYv8uKlomEiLWyMAAt8wAAJRyulKkAKSAAE5UddaLwQ"],
            6: ["DQACAgIAAxkDAAMSZFzzsJzf6z6P4vmdoJoinA_uXHQAAtcwAAJRyulKdVgLh32KAR4vBA",
                "DQACAgIAAxkDAAMPZFzzp-gP1SOuZxAoKvioAXIIWAkAAtQwAAJRyulKlPzHe1IIdqcvBA"],
            # 7: "",
            # 8: "",
            # 9: "",
            # 10: "",
        }

        self.dops = {

            "hello_start": "DQACAgIAAxkDAAMQZFzzq23_TT1zz9MRTPPOHhNt1awAAtUwAAJRyulKJj1s-wM3TzYvBA",
            "hello_go": "DQACAgIAAxkDAAMTZFzzuliInObcSdfPinxOD5-kDosAAtkwAAJRyulKB3Q4Ka8jVoIvBA",
            "answer_true": ["DQACAgIAAxkDAAMRZFzzrbw7G8Prae-L-cvlHPOwhKIAAtYwAAJRyulKeOANO793-d8vBA",
                            "DQACAgIAAxkDAAMUZFzzwJ63kkykDwYLrkqS-pIlbq8AAtowAAJRyulKPDXhmkr11xovBA",
                            "DQACAgIAAxkDAAMHZFzzSKPL_7qatAuVmNHtKD_mWhMAAsowAAJRyulKAQ1gYgw5Ga0vBA"],
            "goodbye": "DQACAgIAAxkDAAMcZFz0RKpUlFOnuIRcFFgVE1_gzx0AAuYwAAJRyulKORG1gWIJv9UvBA",
            "answer_false": ["DQACAgIAAxkDAAMNZFzznzBYe8FEZ4QQXYtlOzQLytYAAtIwAAJRyulK1P79xKm9OfQvBA"],
            # 6: "",
            # 7: "",
            # 8: "",
            # 9: "",
            # 10: "",
        }