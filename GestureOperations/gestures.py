from AppOperations.MailOperations import MailOperation
import time
import traceback


def check_date(input_date):
    try:
        time.strptime(input_date, "%Y-%m-%d")
        return 1
    except Exception:
        return 0

#
# if keywords["ALL"]:
#         search_keyword.append("ALL")
#     for label_time in ["BEFORE", "ON", "SINCE"]:
#         if keywords[label_time]:
#             if check_date(keywords[label_time]):
#                 search_keyword.append(label_time + " " + keywords[label_time])
#             else:
#                 self.speech.speech("Wrong Date! Try again.")
#                 return 0
#
#     for label_text in ["SUBJECT", "BODY", "TEXT", "FROM", "TO", "CC", "BCC"]:
#         if keywords[label_text]:
#             search_keyword.append(label_text + " " + keywords[label_text])
#
#     for label_bool in ["SEEN", "UNSEEN", "ANSWERED", "UNANSWERED", "DELETED", "UNDELETED", "DRAFT", "UNDRAFT",
#                        "FLAGGED", "UNFLAGGED"]:
#         if keywords[label_bool]:
#             search_keyword.append(label_bool)





if __name__ == "__main__":
    pass