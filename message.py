from user import User


class Message:

    def __init__(self, postureType, user):
        self.postureType = postureType
        self.user = user
        self.message = self.adapt_message()

    def overall_posture(self):
        strike = 0
        # the bareme represent the max number of period where the user can have a bad posture before considering
        # the session was bad overall
        bareme_good = 0.2*len(self.postureType.values())
        bareme_bad = 0.5*len(self.postureType.values())
        for value in self.postureType.values():
            if value != "perfect":
                strike+=1
            else:
                pass
        if strike > bareme_good:
            if strike > bareme_bad:
                return "horrible"
            else:
                return "bad"
        else:
            return "good"
        

            
    def adapt_message(self):
        if self.overall_posture() == "bad":
            message = "There's room for improvement "+ User.currentUser +", \n \nYour posture was pretty good, but during some time periods, your position drifted away from the one we set for ourselves.\
Make sure that your back is resting on the back of your chair and straighten your upper back. Your buttocks should touch the back of your chair.\n\n\
When adopting a bad posture, you put an additionnal load on the lumbar region of your spine, which created damages to the soft tissues, and that's when you start to feel pain to your back.\n\n\
Don't forget to get up and move around a few minutes per hour! Even the strongest muscles needs to relax once in a while."

        elif self.overall_posture() == "horrible":
            message = "There's room for improvement "+ User.currentUser +", \n \nThroughout the session, your posture drifted away from the one we set for ourselves.\
Make sure that your back is resting on the back of your chair and straighten your upper back. Your buttocks should touch the back of your chair.\n\n\
When adopting a bad posture, you put an additionnal load on the lumbar region of your spine, which created damages to the soft tissues, and that's when you start to feel pain to your back.\n\n\
Don't forget to get up and move around a few minutes per hour! Even the strongest muscles needs to relax once in a while."

        else:
            message = "Congratulations " + User.currentUser+",\n\nYour posture was really good throughout the session!  \n\n\
By sitting this way, the load on your spine is minimized, especially in the lumbar region, avoiding damages to the supporting soft tissues of your back.\n\n\
Don't forget to get up and move around a few minutes per hour! Even the strongest muscles needs to relax once in a while."

        return message

