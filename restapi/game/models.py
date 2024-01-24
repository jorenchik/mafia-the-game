from django.db import models
from django.contrib.auth.models import User
import datetime


class Action(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)


class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_path = models.CharField(max_length=255, unique=True)
    added_at = models.DateTimeField(default=datetime.datetime.now)


class AccountStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=255, unique=True)


class RoomStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=255, unique=True)


class PlayerStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=255, unique=True)


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default='', blank=True)
    last_name = models.CharField(max_length=255, default='', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio_info = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    is_email_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    account_status = models.ForeignKey(AccountStatus, on_delete=models.CASCADE)
    image = models.ForeignKey(Image,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)
    is_default = models.BooleanField(default=False)
    is_mafia = models.BooleanField(default=False)
    image = models.ForeignKey(Image,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class GameSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Room(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    game_start_time = models.DateTimeField(null=True, blank=True)
    game_end_time = models.DateTimeField(null=True, blank=True)
    access_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    status = models.ForeignKey(RoomStatus, on_delete=models.CASCADE)
    game_setting = models.ForeignKey(GameSetting, on_delete=models.CASCADE)


class GameEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    night_order = models.SmallIntegerField(default=0)
    type = models.CharField(max_length=255, null=True, blank=True)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    timer = models.DurationField(null=True, blank=True)
    activity = models.ForeignKey(Action, on_delete=models.CASCADE)


class Player(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_killed = models.BooleanField(default=False)
    is_voted_out = models.BooleanField(default=False)
    is_room_creator = models.BooleanField(default=False)
    status = models.ForeignKey(PlayerStatus, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    role = models.ForeignKey(Role,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    is_mafia_chat = models.BooleanField(default=False)
    is_modified = models.BooleanField(default=False)
    author = models.ForeignKey(Player, on_delete=models.CASCADE)


class PlayerDenyAllowActivity(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    activity = models.ForeignKey(Action, on_delete=models.CASCADE)
    is_allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('player', 'activity')


class PlayerTriggerEvent(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_event = models.ForeignKey(GameEvent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('player', 'game_event')


class PlayerInfluenceEvent(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_event = models.ForeignKey(GameEvent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('player', 'game_event')


class GameSettingRoles(models.Model):
    game_setting = models.ForeignKey(GameSetting, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    count = models.SmallIntegerField(default=1)

    class Meta:
        unique_together = ('game_setting', 'role')


class RoleActivities(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    activity = models.ForeignKey(Action, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'activity')


class EventInfluencePlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_event = models.ForeignKey(GameEvent, on_delete=models.CASCADE)
    is_allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('player', 'game_event')


class Reply(models.Model):
    id = models.BigAutoField(primary_key=True)
    write = models.ForeignKey(Chat,
                              on_delete=models.CASCADE,
                              related_name='write_reply')
    reply = models.ForeignKey(Chat,
                              on_delete=models.CASCADE,
                              related_name='reply_reply')
