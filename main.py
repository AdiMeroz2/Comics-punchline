import os
import jsonlines
import json
import openai
from openai.api_resources import fine_tune
from pytesseract import Output, pytesseract
import cv2
from PIL import Image, ImageFont, ImageDraw

# fine_tuning.jsonl: file-KJJnk13jHyPDwBWKE5qJaUNI
# Created fine-tune: ft-UlkfRCWIpCaLpbh8b1T6bxSp

# FINE_TUNED_MODEL="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"

openai.api_key = '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'

def prepare_test(test_json):
    with open("fine_tuning.jsonl") as json_file:
        test_data = json.load(json_file)
    return test_data


def zeroShot(givenComic):
    response = openai.Completion.create(
        # model="FINE_TUNED_MODEL",
        engine="text-davinci-002",
        prompt=givenComic,
        temperature=0.4,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

#todo using this
def FewShotConversationComicLeft(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{It is snowing out side, Complete the conversation:\nboy looks outside:Should I stay inside or go outside?\nboy:It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...\nmom kicks the boy out:[complete]\nboy:The more indecisive I am, the faster things get decided.\n} --> {boy looks outside:Should I stay inside or go outside?\nboy:It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...\nmom kicks the boy out:Go out and close the door!\nboy:The more indecisive I am, the faster things get decided.\n}, "
        "{The boy was cuiries where do babies come from, Complete the conversation:\nboy:Do you know where babies come from?\nfriend:[complete]\nboy:Well, I wonder how one finds out!\nfriend checks the label on the cloth:[complete]\nfriend:[complete]\n} --> {boy:Do you know where babies come from?\nfriend:Nope.\nboy:Well, I wonder how one finds out!\nfriend checks the label on the cloth:Here, let me see the back of your shirt.\nfriend:You came from Taiwan.\n}, "
        "{A boy built a new house for his dog, Complete the conversation:\nboy showing the new house:There you are, your new house is all finished..\nboy:Well, What do you think?\ndog looks at the new house and snifs:[complete]\n} --> {boy showing the new house:There you are, your new house is all finished..\nboy:Well, What do you think?\ndog looks at the new house and snifs:It's beautiful!\n}, "
        "{It was raining outside, Complete the conversation:\nboy looking outside:Still raining,huh?\nboy:what do you plan to do all afternoon?\nfriend turns on the TV:[complete]\nfriend sits on the couch:[complete]\n} --> {boy looking outside:Still raining,huh?\nboy:what do you plan to do all afternoon?\nfriend turns on the TV:The obvious...sit in front of the TV\nfriend sits on the couch:And pork on chocolate chip cookie\n}, "
        "{A boy was playing the piano\nConplete the conversation:\ngirl:[If we were married, and you played golf, I’d hate your golf clubs!]\ngirl continuing:[If you drove a sports car, I’d hate your sports car!]\nboy still playing the piano:[complete]\ngirl kicking the piano:[I hate your piano!]\n} --> {girl: If we were married, and you played golf, I’d hate your golf clubs!\ngirl continuing: If you drove a sports car, I’d hate your sports car!\nboy still playing the piano: So?\ngirl kicking the piano: I hate your piano!\n}, "
        + givenComic,
        temperature=0.4,
        max_tokens=200,
        top_p=0,
        frequency_penalty=1,
        presence_penalty=1
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

#todo using this
def FewShotConversationComicRight(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{It is snowing out side, Complete the conversation:\nboy looks outside:[complete]\nboy:[complete]\nmom kicks the boy out:Go out and close the door!\nboy:[complete]\n} --> {boy looks outside:Should I stay inside or go outside?\nboy:It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...\nmom kicks the boy out:Go out and close the door!\nboy:The more indecisive I am, the faster things get decided.\n}, "
        "{The boy was cuiries where do babies come from\nComplete the conversation:\nboy:[complete]\nfriend:Nope.\nboy:[complete]\nfriend checks the label on the cloth:Here, let me see the back of your shirt.\nfriend:You came from Taiwan.\n} --> {boy:Do you know where babies come from?\nfriend:Nope.\nboy:Well, I wonder how one finds out!\nfriend checks the label on the cloth:Here, let me see the back of your shirt.\nfriend:You came from Taiwan.\n}, "
        "{A boy built a new house for his dog\nComplete the conversation:\nboy showing the new house:[complete]\nboy:[complete]\ndog looks at the new house and cries:It's beautiful!\n} --> {boy showing the new house:There you are, your new house is all finished..\nboy:Well, What do you think?\ndog looks at the new house and cries:It's beautiful!\n}, "
        "{It was raining outside\nComplete the conversation:\nboy looking outside:[complete]\nboy:[complete]\nfriend turns on the TV:The obvious...sit in front of the TV\nfriend sits on the couch:And pork on chocolate chip cookie\n} --> {boy looking outside:Still raining,huh?\nboy:what do you plan to do all afternoon?\nfriend turns on the TV:The obvious...sit in front of the TV\nfriend sits on the couch:And pork on chocolate chip cookie\n}, "
        "{A boy was playing the piano\nConplete the conversation:\ngirl:[complete]\ngirl continuing:[complete]\nboy still playing the piano:So?\ngirl kicking the piano:[complete]\n} --> {girl: If we were married, and you played golf, I’d hate your golf clubs!\ngirl continuing: If you drove a sports car, I’d hate your sports car!\nboy still playing the piano: So?\ngirl kicking the piano: I hate your piano!\n}, "
        + givenComic,
        temperature=0.4,
        max_tokens=200,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def FewShotMovment(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{It's snowing out side, Complete the conversation - (boy:[Should I stay inside or go outside?], boy:[It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...], mom kicks the boy out:[complete], boy:[The more indecisive I am, the faster things get decided.]) --> "
        "(boy:[Should I stay inside or go outside?], boy:[It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...], mom kicks the boy out:[Go out and close the door!], boy:[The more indecisive I am, the faster things get decided.])},"
        "{A boy can't find his jacket anywhere, Complete the conversation: (boy:[complete], boy looks uder the bed:[I've looked everywhere! under the bed, over my chair...], boy:[on the stairs, on the floor, in the kitchen... It's just not anywhere!], boy opens the closet:[complete]) --> "
        "(boy:[Where's my jacket?], boy looks uder the bed:[I've looked everywhere! under the bed, over my chair...], boy:[on the stairs, on the floor, in the kitchen... It's just not anywhere!], boy opens the closet:[Oh, here it is! who put it in the stupit closet ?!?])}"
        "{A boy is showing his dog it's new house, Complete the conversation - (boy:[There you are, your new house is all finished..], boy:[Well, What do you think?], dog looks at the new house:[complete]) --> "
        "(boy:[There you are, your new house is all finished..], boy:[Well, What do you think?], dog looks at the new house:[It's beautiful!])}"
        "{A boy is curious about babies, Complete the conversation: (boy:[Do you know where babies come from?], friend:[complete], boy:[well, I wonder how one finds out!], friend checks the label of the shirt:[complete], friend:[complete]) --> "
        "(boy:[Do you know where babies come from?], friend:[Nope], boy:[well, I wonder how one finds out!], friend checks the label of the shirt:[Here, let me see the back of your shirt], friend:[you came from Taiwan.])}"
        + givenComic,
        temperature=0.4,
        max_tokens=200,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def FewShotEmptyConversationComic(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{It's snowing out side , Complete the conversation - boy:[complete], boy:[complete], mom:[complete], boy:[complete]} --> {boy:[Should I stay inside or go outside?], boy:[It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...], mom:[Go out and close the door!], boy:[The more indecisive I am, the faster things get decided.]}, "
        "{A boy is asking a man why grown ups don't go out to play, Complete the conversation - boy:[complete], man:[complete], boy:[complete], man:[complete], boy:[complete], man:[complete]} --> {boy:[how come grown ups don't go out to play?], man:[Grown ups can only justify playing outside by calling it exercise, doing it when they'd rather not, and keeping records to quantify their performance.], boy:[That sound like a job.], man:[Except you don't get paid], boy:[so play is worse than work?], man:[Being a grown up is tough.]}, "
        "{A boy can't find his jacket anywhere in the house, Complete the conversation - boy:[complete], boy:[complete], boy:[complete], boy:[complete]} --> {boy:[Where's my jacket?], boy:[I've looked everywhere! under the bed, over my chair...], boy:[on the stairs, on the floor, in the kitchen... It's just not anywhere!], boy:[Oh, here it is! who put it in the stupid closet ?!?]}, "
        "{The boy is tired in the morning and can't sleep at night, Complete the conversation - boy:[complete], boy:[complete], boy:[complete], boy:[complete] --> {boy:[No! No! No! I need more sleep!], boy:[I can't keep my eyes open], boy:[Bed?! already?! but i'm awake!!], boy:[my internal clock in on tokyo time.]}, "
        "{A boy is curies about where do babies come from, Complete the conversation - boy:[complete], friend:[complete], boy:[complete], friend:[complete], friend:[complete]} --> {boy:[Do you know where babies come from?], friend:[Nope.], boy:[Well, I wonder how one finds out!], friend:[Here, let me see the back of your shirt.], friend:[You came from Taiwan.]}, "
        "{A boy is in the zoo, Complete the conversation - boy:[complete], boy:[complete], woman:[complete], boy:[complete], woman:[complete] boy:[complete]} --> {boy:[Hey, those kids are feeding the animals!], boy:[Mom, can I get some peanuts to feed the animals?], woman:[I'm not your mom], boy:[Whoop!], woman:[Are you Lost?, what does your mom look like?], boy:[From the knees down she looks just like you.]}, "
         + givenComic,
        temperature=0,
        max_tokens=200,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def FewShotEmptyConversationComic2(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{It's snowing out side , Complete the conversation in the following order: (1.boy, 2.boy , 3.mom , 4.boy )} --> {boy:[Should I stay inside or go outside?], boy:[It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...], mom:[Go out and close the door!], boy:[The more indecisive I am, the faster things get decided.]}, "
        "{A boy is asking a man why grown ups don't go out to play, Complete the conversation in the following order: (1.boy , 2.man , 3.boy , 4.man , 5.boy , 6.man )} --> {boy:[how come grown ups don't go out to play?], man:[Grown ups can only justify playing outside by calling it exercise, doing it when they'd rather not, and keeping records to quantify their performance.], boy:[That sound like a job.], man:[Except you don't get paid], boy:[so play is worse than work?], man:[Being a grown up is tough.]}, "
        "{A boy can't find his jacket anywhere in the house, Complete the conversation in the following order: (1.boy , 2.boy , 3.boy , 4.boy )} --> {boy:[Where's my jacket?], boy:[I've looked everywhere! under the bed, over my chair...], boy:[on the stairs, on the floor, in the kitchen... It's just not anywhere!], boy:[Oh, here it is! who put it in the stupid closet ?!?]}, "
        "{The boy is tired in the morning and can't sleep at night, Complete the conversation in the following order: (1.boy , 2.boy , 3.boy , 4.boy )} --> {boy:[No! No! No! I need more sleep!], boy:[I can't keep my eyes open], boy:[Bed?! already?! but i'm awake!!], boy:[my internal clock in on tokyo time.]}, "
        "{A boy is curies about where do babies come from, Complete the conversation in the following order: (1.boy, 2.friend , 3.boy , 4.friend: , 5.friend )} --> {boy:[Do you know where babies come from?], friend:[Nope.], boy:[Well, I wonder how one finds out!], friend:[Here, let me see the back of your shirt.], friend:[You came from Taiwan.]}, "
        "{A boy is in the zoo, Complete the conversation in the following order: (1.boy , 2.boy , 3.woman , 4.boy , 5.woman, 6.boy)} --> {boy:[Hey, those kids are feeding the animals!], boy:[Mom, can I get some peanuts to feed the animals?], woman:[I'm not your mom], boy:[Whoop!], woman:[Are you Lost?, what does your mom look like?], boy:[From the knees down she looks just like you.]}, "
        + givenComic,
        temperature=0,
        max_tokens=200,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def FewShotEmptyConversationComic3(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{title:[Hard to decide], content:[It is snowing out side], Complete the conversation - boy:[complete], boy:[complete], mom:[complete], boy:[complete]} --> {boy:[Should I stay inside or go outside?], boy:[It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...], mom:[Go out and close the door!], boy:[The more indecisive I am, the faster things get decided.]}, "
        "{title:[grown ups], content:[The boy went up to a man for a question], Complete the conversation - boy:[complete], man:[complete], boy:[complete], man:[complete], boy:[complete], man:[complete]} --> {boy:[how come grown ups don't go out to play?], man:[Grown ups can only justify playing outside by calling it exercise, doing it when they'd rather not, and keeping records to quantify their performance.], boy:[That sound like a job.], man:[Except you don't get paid], boy:[so play is worse than work?], man:[Being a grown up is tough.]}, "
        "{title:[Where is my jacket], content:[The boy couldn't find his jacket], Complete the conversation - boy:[complete], boy:[complete], boy:[complete], boy:[complete]} --> {boy:[Where's my jacket?], boy:[I've looked everywhere! under the bed, over my chair...], boy:[on the stairs, on the floor, in the kitchen... It's just not anywhere!], boy:[Oh, here it is! who put it in the stupid closet ?!?]}, "
        "{title:[sleeping problems], content:[The boy was tired in the morning and awake at night], Complete the conversation - boy:[complete], boy:[complete], boy:[complete], boy:[complete] --> {boy:[No! No! No! I need more sleep!], boy:[I can't keep my eyes open], boy:[Bed?! already?! but i'm awake!!], boy:[my internal clock in on tokyo time.]}, "
        "{title:[babies], content:[The boy was cuiries where do babies come from], Complete the conversation - boy:[complete], friend:[complete], boy:[complete], friend:[complete], friend:[complete]} --> {boy:[Do you know where babies come from?], friend:[Nope.], boy:[Well, I wonder how one finds out!], friend:[Here, let me see the back of your shirt.], friend:[You came from Taiwan.]}, "
        "{title:[mom?], content:[the boy was in the zoo], Complete the conversation - boy:[complete], boy:[complete], woman:[complete], boy:[complete], woman:[complete] boy:[complete]} --> {boy:[Hey, those kids are feeding the animals!], boy:[Mom, can I get some peanuts to feed the animals?], woman:[I'm not your mom], boy:[Whoop!], woman:[Are you Lost?, what does your mom look like?], boy:[From the knees down she looks just like you.]}, "
        + givenComic,
        temperature=0.4,
        max_tokens=200,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=1
    )

    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

#todo using this
def FewShotEmptyMovement1(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{title - hard to decide\ncontent - It is snowing out side\nComplete the conversation:\nboy looks outside:[complete]\nboy:[complete]\nmom kicks the boy out:[complete]\nboy:[complete]\n} --> {boy looks outside:Should I stay inside or go outside?\nboy:It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...\nmom kicks the boy out:Go out and close the door!\nboy:The more indecisive I am, the faster things get decided.\n}, "
        "{title - missing jacket\ncontent - The boy couldn't find his jacket\nComplete the conversation:\nboy shouts:[complete]\nboy looks under the bed:[complete]\nboy:[complete]\nboy opens the closet:[complete]\n} --> {boy shouts:Where's my jacket?\nboy looks under the bed:I've looked everywhere! under the bed, over my chair...\nboy:on the stairs, on the floor, in the kitchen... It's just not anywhere!\nboy opens the closet:Oh, here it is! who put it in the stupid closet ?!?\n}, "
        "{title - babies\ncontent - The boy was cuiries where do babies come from\nComplete the conversation:\nboy:[complete]\nfriend:[complete]\nboy:[complete]\nfriend checks the label on the cloth:[complete]\nfriend:[complete]\n} --> {boy:Do you know where babies come from?\nfriend:Nope.\nboy:Well, I wonder how one finds out!\nfriend checks the label on the cloth:Here, let me see the back of your shirt.\nfriend:You came from Taiwan.\n}, "
        "{title - new home\ncontent - A boy built a new house for his dog\nComplete the conversation:\nboy showing the new house:[complete]\nboy:[complete]\ndog looks at the new house and snifs:[complete]\n} --> {boy showing the new house:There you are, your new house is all finished..\nboy:Well, What do you think?\ndog looks at the new house and snifs:It's beautiful!\n}, "
        "{title - plans for the afternoon\ncontent - It was raining outside\nComplete the conversation:\nboy looking outside:[complete]\nboy:[complete]\nfriend turns on the TV:[complete]\nfriend sits on the couch:[complete]\n} --> {boy looking outside:Still raining,huh?\nboy:what do you plan to do all afternoon?\nfriend turns on the TV:The obvious...sit in front of the TV\nfriend sits on the couch:And pork on chocolate chip cookie\n}, "
        "{title - If we were married\ncontent - A boy was playing the piano\nConplete the conversation:\ngirl:[complete]\ngirl continuing:[complete]\nboy still playing the piano:[complete]\ngirl kicking the piano:[complete]\n} --> {girl: If we were married, and you played golf, I’d hate your golf clubs!\ngirl continuing: If you drove a sports car, I’d hate your sports car!\nboy still playing the piano: So?\ngirl kicking the piano: I hate your piano!\n}, "
        + givenComic,
        temperature=0.4,
        max_tokens=200,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def FewShotEmptyMovement2(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "{title:[Hard to decide], content:[It is snowing out side], Complete the conversation - boy looks outside:[complete]\n, boy:[complete]\n, mom kicks the boy out:[complete]\n, boy:[complete]} --> {boy looks outside:[Should I stay inside or go outside?]\n, boy:[It's awfully cold out, but I suppose I could bundle up. It looks windy though. But still, I'd like to go sledding. Then agian, Maybe I'd rather stay in on the other hand...]\n, mom kicks the boy out:[Go out and close the door!]\n, boy:[The more indecisive I am, the faster things get decided.]\n}, "
        "{title:[Where is my jacket], content:[The boy couldn't find his jacket], Complete the conversation - boy shouts:[complete]\n, boy looks under the bed:[complete]\n, boy:[complete]\n, boy opens the closet:[complete]} --> {boy shouts:[Where's my jacket?]\n, boy looks under the bed:[I've looked everywhere! under the bed, over my chair...]\n, boy:[on the stairs, on the floor, in the kitchen... It's just not anywhere!]\n, boy opens the closet:[Oh, here it is! who put it in the stupid closet ?!?]\n}, "
        "{title:[babies], content:[The boy was cuiries where do babies come from], Complete the conversation - boy:[complete]\n, friend:[complete]\n, boy:[complete]\n, friend checks the label on the cloth:[complete]\n, friend:[complete]} --> {boy:[Do you know where babies come from?]\n, friend:[Nope.]\n, boy:[Well, I wonder how one finds out!]\n, friend checks the label on the cloth:[Here, let me see the back of your shirt.]\n, friend:[You came from Taiwan.]\n}, "
        "{title:[new home], content:[A boy built a new house for his dog], Complete the conversation - boy showing the new house:[complete]\n, boy:[complete]\n, dog looks at the new house, dog snifs:[complete]} --> {boy showing the new house:[There you are, your new house is all finished..]\n, boy:[Well, What do you think?]\n, dog looks at the new house, dog snifs:[It's beautiful!]\n}"
        "{title:[bark], content:[A boy is asking his dog a question], Complete the conversation - boy:[complete]\n, dog toss a coin, dog looks at the result, dog:[complete]} --> {boy:[When someone walks by, how do you decide if you should bark at him?]\n, dog toss a coin, dog looks at the result, dog:[Woof!]}"
        + givenComic,
        temperature=0.4,
        max_tokens=200,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def CalvinAndDadHigh10(givenComic):
    response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=
            "Complete the conversation:\n{Calvin:Somewhere in communist Russia I'll bet there's a little boy who has never know anything but censorship\nCalvin:But maybe he's heard about America, and he dreams of living in this land of freedom and opportunity!\nCalvin:Someday, I'd like to meet that little boy\nCalvin:And tell him the awful truth about this place!!!\nDad:\n} --> {Dad: Calvin, be quiet and eat the lima beans.\n}, "   
            "Complete the conversation:\n{Dad:Watching a Christmas special?\nCalvin:Yep.\nDad:Another show extolling love and peace interrupted every seven minutes by commercials extolling greed and waste.\nDad:I hate to think what you are learning from this.\nCalvin:\n} --> {Calvin: I'm learning I need my own TV so I can watch someplace else.\n}, "
            "Complete the conversation:\n{Dad answering the phone:Hello?\nCalvin:hi dad, it's me\nDad:You're supposed to be at school!\nCalvin:I am at school.\nDad:Are you all right? what's the matter? Why are you calling?\nCalvin:\n} --> {Calvin: I told the teacher I had to go to the bathroom. Quick, what's 11+7?\n}, "
            "Complete the conversation:\n{Calvin:Hey dad, how does a carburetor work?\nDad:I can't tell you.\nCalvin: Why not?\nDad:It's a secret\nCalvin:\n} --> {Calvin:No it isn't! You just don't know!\n}, "
            "Complete the conversation:\n{Dad:Calvin, How do you explain this test score? It's terrible!\nCalvin:I didn't study for it.\nDad:What do you mean you didn't study for it? why not?\nCalvin:I forgot.\nDad shouts:You forgot? How could you possibly forget??\nCalvin:What?Where am I? Who am I?\nDad shouts:\n} --> {Dad shouts:Don't give me this amnesia stuff!!\n}, "
            "Complete the conversation:\n{Calvin:Your polls are slipping dad, better get with it.\nDad:Calvin, being your dad is not an elected position, I don't have to respond to polls.\nCalvin:Not elected? You mean you can govern with dictatorial impunity?\nDad:Exactly.\nCalvin:In short, open revolt and exile is the only hope for change?\nDad:\n} --> {Dad:I don't like the direction this is going.\n}, "
            "Complete the conversation:\n{Calvin:Why does ice float?\nDad:Because its cold, ice wants to get warm, so it goes to the top of the liquid in order to be nearer to the sun.\nCalvin:Is that true?\nDad:Look it up and find out.\nCalvin:I should just look stuff up in the first place.\nDad:\n} --> {Dad: You can learn A lot talking to me.\n}, "
            "Complete the conversation:\n{Calvin:What's this?\nDad:Taste it, you'll love it.\nCalvin pushed the food away:\n} --> {Calvin pushed the food away:You know you'll hate something when they don't tell you what it is.\n}, "
            "Complete the conversation:\n{Calvin:Hey Dad, I'll guess any number you're thinking of! Go ahead, pick a number!\nDad: MM..ok, I've got it.\nCalvin:Is it 92, 376,051?\nDad:By golly, it is!\nCalvin:Wait a minute! you're just trying to get rid of me, aren't you?!\nDad:\n} --> {Dad:No, you're Psychic. Go show mom.}\n, "
            "Complete the conversation:\n{Calvin:I've got an idea, dad.\nCalvin:Maybe I'd get better grades if you offered me one dollar for every 'D', five dollars for every 'C', ten dollars for every 'B', and fifteen dollars for every 'A'!\nDad:I'm not going to bride you Calvin, you should apply yourself for your own good\nCalvin:\n} --> {Calvin:I thought I could make an easy four buckets.\n}, "
            + givenComic,
            temperature=1,
            max_tokens=200,
            top_p=1,
            frequency_penalty=2,
            presence_penalty=2
        )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def CalvinAndDadLow10(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "Complete the conversation:\n{Calvin:Somewhere in communist Russia I'll bet there's a little boy who has never know anything but censorship\nCalvin:But maybe he's heard about America, and he dreams of living in this land of freedom and opportunity!\nCalvin:Someday, I'd like to meet that little boy\nCalvin:And tell him the awful truth about this place!!!\nDad:\n} --> {Dad: Calvin, be quiet and eat the lima beans.\n}, "
        "Complete the conversation:\n{Dad:Watching a Christmas special?\nCalvin:Yep.\nDad:Another show extolling love and peace interrupted every seven minutes by commercials extolling greed and waste.\nDad:I hate to think what you are learning from this.\nCalvin:\n} --> {Calvin: I'm learning I need my own TV so I can watch someplace else.\n}, "
        "Complete the conversation:\n{Dad answering the phone:Hello?\nCalvin:hi dad, it's me\nDad:You're supposed to be at school!\nCalvin:I am at school.\nDad:Are you all right? what's the matter? Why are you calling?\nCalvin:\n} --> {Calvin: I told the teacher I had to go to the bathroom. Quick, what's 11+7?\n}, "
        "Complete the conversation:\n{Calvin:Hey dad, how does a carburetor work?\nDad:I can't tell you.\nCalvin: Why not?\nDad:It's a secret\nCalvin:\n} --> {Calvin:No it isn't! You just don't know!\n}, "
        "Complete the conversation:\n{Dad:Calvin, How do you explain this test score? It's terrible!\nCalvin:I didn't study for it.\nDad:What do you mean you didn't study for it? why not?\nCalvin:I forgot.\nDad shouts:You forgot? How could you possibly forget??\nCalvin:What?Where am I? Who am I?\nDad shouts:\n} --> {Dad shouts:Don't give me this amnesia stuff!!\n}, "
        "Complete the conversation:\n{Calvin:Your polls are slipping dad, better get with it.\nDad:Calvin, being your dad is not an elected position, I don't have to respond to polls.\nCalvin:Not elected? You mean you can govern with dictatorial impunity?\nDad:Exactly.\nCalvin:In short, open revolt and exile is the only hope for change?\nDad:\n} --> {Dad:I don't like the direction this is going.\n}, "
        "Complete the conversation:\n{Calvin:Why does ice float?\nDad:Because its cold, ice wants to get warm, so it goes to the top of the liquid in order to be nearer to the sun.\nCalvin:Is that true?\nDad:Look it up and find out.\nCalvin:I should just look stuff up in the first place.\nDad:\n} --> {Dad: You can learn A lot talking to me.\n}, "
        "Complete the conversation:\n{Calvin:What's this?\nDad:Taste it, you'll love it.\nCalvin pushed the food away:\n} --> {Calvin pushed the food away:You know you'll hate something when they don't tell you what it is.\n}, "
        "Complete the conversation:\n{Calvin:Hey Dad, I'll guess any number you're thinking of! Go ahead, pick a number!\nDad: MM..ok, I've got it.\nCalvin:Is it 92, 376,051?\nDad:By golly, it is!\nCalvin:Wait a minute! you're just trying to get rid of me, aren't you?!\nDad:\n} --> {Dad:No, you're Psychic. Go show mom.}\n, "
        "Complete the conversation:\n{Calvin:I've got an idea, dad.\nCalvin:Maybe I'd get better grades if you offered me one dollar for every 'D', five dollars for every 'C', ten dollars for every 'B', and fifteen dollars for every 'A'!\nDad:I'm not going to bride you Calvin, you should apply yourself for your own good\nCalvin:\n} --> {Calvin:I thought I could make an easy four buckets.\n}, "
        + givenComic,
        temperature=0,
        max_tokens=200,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def CalvinAndDadLow3(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "Complete the conversation:\n{Dad:Watching a Christmas special?\nCalvin:Yep.\nDad:Another show extolling love and peace interrupted every seven minutes by commercials extolling greed and waste.\nDad:I hate to think what you are learning from this.\nCalvin:\n} --> {Calvin: I'm learning I need my own TV so I can watch someplace else.\n}, "
        "Complete the conversation:\n{Calvin:Hey dad, how does a carburetor work?\nDad:I can't tell you.\nCalvin: Why not?\nDad:It's a secret\nCalvin:\n} --> {Calvin:No it isn't! You just don't know!\n}, "
        "Complete the conversation:\n{Calvin:I've got an idea, dad.\nCalvin:Maybe I'd get better grades if you offered me one dollar for every 'D', five dollars for every 'C', ten dollars for every 'B', and fifteen dollars for every 'A'!\nDad:I'm not going to bride you Calvin, you should apply yourself for your own good\nCalvin:\n} --> {Calvin:I thought I could make an easy four buckets.\n}, "
        "Complete the conversation:\n{Dad answering the phone:Hello?\nCalvin:hi dad, it's me\nDad:You're supposed to be at school!\nCalvin:I am at school.\nDad:Are you all right? what's the matter? Why are you calling?\nCalvin:\n} --> {Calvin: I told the teacher I had to go to the bathroom. Quick, what's 11+7?\n}, "
        + givenComic,
        temperature=0,
        max_tokens=200,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]

def CalvinAndDadHigh3(givenComic):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        "Complete the conversation:\n{Dad:Watching a Christmas special?\nCalvin:Yep.\nDad:Another show extolling love and peace interrupted every seven minutes by commercials extolling greed and waste.\nDad:I hate to think what you are learning from this.\nCalvin:\n} --> {Calvin: I'm learning I need my own TV so I can watch someplace else.\n}, "
        "Complete the conversation:\n{Calvin:Hey dad, how does a carburetor work?\nDad:I can't tell you.\nCalvin: Why not?\nDad:It's a secret\nCalvin:\n} --> {Calvin:No it isn't! You just don't know!\n}, "
        "Complete the conversation:\n{Calvin:I've got an idea, dad.\nCalvin:Maybe I'd get better grades if you offered me one dollar for every 'D', five dollars for every 'C', ten dollars for every 'B', and fifteen dollars for every 'A'!\nDad:I'm not going to bride you Calvin, you should apply yourself for your own good\nCalvin:\n} --> {Calvin:I thought I could make an easy four buckets.\n}, "
        "Complete the conversation:\n{Dad answering the phone:Hello?\nCalvin:hi dad, it's me\nDad:You're supposed to be at school!\nCalvin:I am at school.\nDad:Are you all right? what's the matter? Why are you calling?\nCalvin:\n} --> {Calvin: I told the teacher I had to go to the bathroom. Quick, what's 11+7?\n}, "
        + givenComic,
        temperature=1,
        max_tokens=200,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2
    )
    context = response.choices[0].text.split('.')
    print(context[0])
    return context[0]
# def getTextInImage(image):
#     image = cv2.imread(image)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (9,9), 0)
#     thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
#
#     # Dilate to combine adjacent text contours
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
#     dilate = cv2.dilate(thresh, kernel, iterations=4)
#
#     # Find contours, highlight text areas, and extract ROIs
#     cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#     # print(cnts)
#     # cv2.imshow('Result', img)
#     cv2.imshow('image', image)
#     cv2.waitKey(0)
def breakText(text, size):
    returnText = ""
    counter = 0
    splitText = text.split(" ")
    for s in splitText:
        counter += len(s)
        returnText = returnText + s + " "
        if counter > size:
            returnText += "\n"
            counter = 0
    return returnText

def putTextInImage(image, text, position, name, size):
    img = Image.open(image)
    title_font = ImageFont.truetype('arial.ttf', size)
    image_editable = ImageDraw.Draw(img)
    image_editable.text(position, text, (0, 0, 0), font=title_font)
    img.save(name)

def cleanText(text):
    result = ""
    result_split = text.split(":")
    if len(text) > 1:
        result = result_split[1]
    else:
        result = result_split[0]
    result_split = result.split("}")
    result = result_split[0]
    return result

def example1():
    # print("please select the algorithm:\n0 - zero-shot-learning\n1 - Fine-tuning 1\n2 - Fine-tuning 2")
    selection = input("please select the algorithm:\n0 - zero-shot-learning\n1 - Fine-tuning with more exampes\n2 - Fine-tuning with few exampes\nPlease enter:")
    conversation = "Calvin: Dad, How do soldiers killing each other solve the world's problem?\nDad was speechless.\nCalvin walks away:"
    if selection == "0":
        result = zeroShot("What did Calvin from the comic 'Calvin and Hobbes' said? \n" + conversation)
    elif selection == "1":
        result = CalvinAndDadHigh10("Complete the conversation:\n{" + conversation + "\n} --> ")
    elif selection == "2":
        result = CalvinAndDadHigh10("Complete the conversation:\n{" + conversation + "\n} --> ")
    else:
        print("invalid input")
        return
    # result = "What a wild imagination my son has!"
    result = cleanText(result)
    result = breakText(result, 23)
    if selection == "0":
        putTextInImage("example_1.png", result, (260,300), "result_1.png", 18)
    else:
        putTextInImage("example_1.png", result, (230,300), "result_1.png", 18)


def example2():
    selection = input("please select the algorithm:\n0 - zero-shot-learning\n1 - Fine-tuning with more exampes\n2 - Fine-tuning with few exampes\nPlease enter:")
    conversation = "Calvin:Hey dad, can I take the gas can for the lawn mower out in the back yard?\nDad:What on earth for? It's 8:00 at night!\nCalvin:I want to pour gasline in big letters on the lawn, and set fire to it so airplanes can read is as they fly over!\nDad:No, you can't do that! Don't be ridicilous!\nDad thought to himself:"
    if selection == "0":
        result = zeroShot("What did Calvin's dad from the comic 'Calvin and Hobbes' thought to himself? \n"+conversation)
    elif selection == "1":
        result = CalvinAndDadHigh10("Complete the conversation:\n{" + conversation + "\n} --> ")
    elif selection == "2":
        result = CalvinAndDadHigh3("Complete the conversation:\n{" + conversation + "\n} --> ")
    else:
        print("invalid input")
        return
    result = cleanText(result)
    result = breakText(result, 21)
    putTextInImage("example_2.png", result, (380,440), "result_2.png", 23)

if __name__ == '__main__':
    # example1()
    example2()


    # conversation = "Calvin:I'm freezing! Why do we keep this house so darn cold?!\nCalvin:Crank up the thermostat and build fire, will ya?\nDad:I have a better idea, come here.\nDad opens the door:OK, step outside.\nCalvin:Why? What's outside?\nDad:In a few minutes you can come in, and then the house will seem nice and warm.\nCalvin:"

    # conversation = "Calvin:Why does ice float?\nDad:Because its cold, ice wants to get warm, so it goes to the top of the liquid in order to be nearer to the sun.\nCalvin:Is that true?\nDad:Look it up and find out.\nCalvin:I should just look stuff up in the first place.\nDad:"

    # zeroShot("What did Calvin from the comic 'Calvin and Hobbes' said? \n" + conversation)

    # conversation =
    # conversation = "Dad:Time for bed, Calvin?\nCalvin:You can put my body to bed, but my spirits going to stay right here, so why bother? Why shouldn't I just stay up?.\nDad:Because the body is the home of the spirit, and if you're \nCalvin:"
    # CalvinAndDadHigh10("Complete the conversation:\n{" + conversation + "\n} --> ")
    # CalvinAndDadLow10("Complete the conversation:\n{" + conversation + "\n} --> ")
    # CalvinAndDadHigh3("Complete the conversation:\n{" + conversation + "\n} --> ")
    # CalvinAndDadLow3("Complete the conversation:\n{" + conversation + "\n} --> ")
    # zeroShot("What did Calvin's dad from the comic 'Calvin and Hobbes' said? \n" + conversation)
