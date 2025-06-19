receiver_manifest_content = '''
<receiver android:name="{}.{}"
    android:enabled="true"
    android:exported="true">
</receiver>

<service android:name="{}.{}"
    android:exported="true"
    android:foregroundServiceType="dataSync"/>

<activity android:name="{}.{}"
    android:exported="true">
</activity>

'''

trigger_decode_method_smali = """
.method public static {}({})Ljava/lang/String;
    .registers {}
    {}
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
    {}
        }
        names = {
    {}
        }
    .end annotation

    .line 15
    invoke-static {{}}, L{};->{}({})Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
"""



receiver_smali_code = """
.class public L{}/ApkStringDecodeBroadcastReceiver;
.super Landroid/content/BroadcastReceiver;
.source "ApkStringDecodeBroadcastReceiver.java"


# static fields
.field public static LOG_TAG_STANDARD:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .registers 1

    .line 14
    const-string v0, "DecodeClass"

    sput-object v0, L{}/ApkStringDecodeBroadcastReceiver;->LOG_TAG_STANDARD:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .line 13
    invoke-direct {p0}, Landroid/content/BroadcastReceiver;-><init>()V

    return-void
.end method


# virtual methods
.method public onReceive(Landroid/content/Context;Landroid/content/Intent;)V
    .registers 27
    .param p1, "context"    # Landroid/content/Context;
    .param p2, "intent"    # Landroid/content/Intent;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0
        }
        names = {
            "context",
            "intent"
        }
    .end annotation

    .line 19
    move-object/from16 v10, p1

    move-object/from16 v11, p2

    sget-object v0, L{}/ApkStringDecodeBroadcastReceiver;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeBroadcastReceiver - onReceive - 0"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 20
    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 22
    new-instance v0, Landroid/content/Intent;

    const-class v1, L{}/ApkStringDecodeActivity;

    invoke-direct {v0, v10, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    move-object v12, v0

    .line 23
    .local v12, "activityIntent":Landroid/content/Intent;
    const/high16 v0, 0x10000000

    invoke-virtual {v12, v0}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 25
    invoke-virtual/range {p2 .. p2}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    move-result-object v0

    if-eqz v0, :cond_2a

    .line 26
    invoke-virtual/range {p2 .. p2}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    move-result-object v0

    invoke-virtual {v12, v0}, Landroid/content/Intent;->putExtras(Landroid/os/Bundle;)Landroid/content/Intent;

    .line 29
    :cond_2a
    const-string v0, "key1"

    invoke-virtual {v11, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v13

    .line 30
    .local v13, "value1":Ljava/lang/String;
    const-string v0, "hashmap"

    invoke-virtual {v11, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v14

    .line 31
    .local v14, "encodedJson":Ljava/lang/String;
    const-string v0, "part_number"

    const/4 v1, -0x1

    invoke-virtual {v11, v0, v1}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v15

    .line 32
    .local v15, "partNumber":I
    const-string v0, "total_parts"

    invoke-virtual {v11, v0, v1}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v16

    .line 33
    .local v16, "totalParts":I
    const-string v0, "subpart_number"

    invoke-virtual {v11, v0, v1}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v17

    .line 34
    .local v17, "subpartNumber":I
    const-string v0, "subtotal_parts"

    invoke-virtual {v11, v0, v1}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v18

    .line 35
    .local v18, "totalSubparts":I
    const-string v0, "class_name"

    invoke-virtual {v11, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    .line 36
    .local v9, "className":Ljava/lang/String;
    const-string v0, "method_name"

    invoke-virtual {v11, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    .line 37
    .local v8, "methodName":Ljava/lang/String;
    const-string v0, "java_signature"

    invoke-virtual {v11, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v7

    .line 38
    .local v7, "javaSignature":Ljava/lang/String;
    const-string v0, "ping"

    invoke-virtual {v11, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v19

    .line 39
    .local v19, "triggerPing":Ljava/lang/String;
    const-string v0, "hashmap_read_file"

    invoke-virtual {v11, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v20

    .line 41
    .local v20, "hashmapReadFile":Ljava/lang/String;
    const/16 v0, 0x64

    const-string v1, "max_entries_allowed"

    invoke-virtual {v11, v1, v0}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v21

    .line 43
    .local v21, "maxEntriesAllowed":I
    if-eqz v19, :cond_8e

    invoke-virtual/range {v19 .. v19}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_8e

    .line 44
    sget-object v0, L{}/ApkStringDecodeBroadcastReceiver;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeBroadcastPing Received"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 45
    invoke-static/range {p1 .. p1}, L{}/ApkStringDecodeCommon;->pingCollected(Landroid/content/Context;)V

    move-object v0, v7

    move-object v11, v8

    move-object/from16 v23, v12

    move-object v12, v9

    goto/16 :goto_126

    .line 46
    :cond_8e
    if-eqz v20, :cond_a4

    invoke-virtual/range {v20 .. v20}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_a4

    .line 47
    sget-object v0, L{}/ApkStringDecodeBroadcastReceiver;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeBroadcast - Decode - Root (Error: not working on BroadcastReceiver)"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    move-object v0, v7

    move-object v11, v8

    move-object/from16 v23, v12

    move-object v12, v9

    goto/16 :goto_126

    .line 49
    :cond_a4
    if-eqz v14, :cond_e5

    invoke-virtual {v14}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_e5

    invoke-virtual {v9}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_e5

    if-eqz v8, :cond_e5

    invoke-virtual {v8}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_e5

    if-eqz v7, :cond_e5

    invoke-virtual {v7}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_e5

    .line 50
    sget-object v0, L{}/ApkStringDecodeBroadcastReceiver;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeBroadcast - Decode - BroadcastReceiver/Logcat"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 51
    move-object/from16 v0, p1

    move-object v1, v14

    move v2, v15

    move/from16 v3, v16

    move/from16 v4, v17

    move/from16 v5, v18

    move-object v6, v9

    move-object/from16 v22, v7

    .end local v7    # "javaSignature":Ljava/lang/String;
    .local v22, "javaSignature":Ljava/lang/String;
    move-object v7, v8

    move-object v11, v8

    .end local v8    # "methodName":Ljava/lang/String;
    .local v11, "methodName":Ljava/lang/String;
    move-object/from16 v8, v22

    move-object/from16 v23, v12

    move-object v12, v9

    .end local v9    # "className":Ljava/lang/String;
    .local v12, "className":Ljava/lang/String;
    .local v23, "activityIntent":Landroid/content/Intent;
    move/from16 v9, v21

    invoke-static/range {v0 .. v9}, L{}/ApkStringDecodeCommon;->decodeAllStringsReceiverLogcat(Landroid/content/Context;Ljava/lang/String;IIIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;I)V

    move-object/from16 v0, v22

    goto :goto_126

    .line 49
    .end local v11    # "methodName":Ljava/lang/String;
    .end local v22    # "javaSignature":Ljava/lang/String;
    .end local v23    # "activityIntent":Landroid/content/Intent;
    .restart local v7    # "javaSignature":Ljava/lang/String;
    .restart local v8    # "methodName":Ljava/lang/String;
    .restart local v9    # "className":Ljava/lang/String;
    .local v12, "activityIntent":Landroid/content/Intent;
    :cond_e5
    move-object/from16 v22, v7

    move-object v11, v8

    move-object/from16 v23, v12

    move-object v12, v9

    .line 52
    .end local v7    # "javaSignature":Ljava/lang/String;
    .end local v8    # "methodName":Ljava/lang/String;
    .end local v9    # "className":Ljava/lang/String;
    .restart local v11    # "methodName":Ljava/lang/String;
    .local v12, "className":Ljava/lang/String;
    .restart local v22    # "javaSignature":Ljava/lang/String;
    .restart local v23    # "activityIntent":Landroid/content/Intent;
    if-eqz v13, :cond_118

    invoke-virtual {v13}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_118

    if-eqz v12, :cond_118

    invoke-virtual {v12}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_118

    if-eqz v11, :cond_118

    invoke-virtual {v11}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_118

    move-object/from16 v0, v22

    .end local v22    # "javaSignature":Ljava/lang/String;
    .local v0, "javaSignature":Ljava/lang/String;
    if-eqz v0, :cond_11a

    invoke-virtual {v0}, Ljava/lang/String;->isEmpty()Z

    move-result v1

    if-nez v1, :cond_11a

    .line 53
    sget-object v1, L{}/ApkStringDecodeBroadcastReceiver;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v2, "ApkStringDecodeBroadcast - Decode - Single"

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 54
    invoke-static {v10, v12, v11, v0, v13}, L{}/ApkStringDecodeCommon;->singleDecode(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_126

    .line 52
    .end local v0    # "javaSignature":Ljava/lang/String;
    .restart local v22    # "javaSignature":Ljava/lang/String;
    :cond_118
    move-object/from16 v0, v22

    .line 56
    .end local v22    # "javaSignature":Ljava/lang/String;
    .restart local v0    # "javaSignature":Ljava/lang/String;
    :cond_11a
    sget-object v1, L{}/ApkStringDecodeBroadcastReceiver;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v2, "Error: BroadcastReceiver Parameter missing"

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 57
    sget-object v1, Ljava/lang/System;->out:Ljava/io/PrintStream;

    invoke-virtual {v1, v2}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 60
    :goto_126
    return-void
.end method
"""

activity_smali_code= """
.class public L{}/ApkStringDecodeActivity;
.super Landroid/app/Activity;
.source "ApkStringDecodeActivity.java"


# static fields
.field public static LOG_TAG_STANDARD:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .registers 1

    .line 19
    const-string v0, "DecodeClass"

    sput-object v0, L{}/ApkStringDecodeActivity;->LOG_TAG_STANDARD:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .line 18
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .registers 6
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "savedInstanceState"
        }
    .end annotation

    .line 24
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 25
    sget-object v0, L{}/ApkStringDecodeActivity;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeActivity - onCreate - 0"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 26
    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 28
    new-instance v0, Landroid/widget/LinearLayout;

    invoke-direct {v0, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    .line 29
    .local v0, "layout":Landroid/widget/LinearLayout;
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setOrientation(I)V

    .line 30
    const/16 v1, 0x11

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setGravity(I)V

    .line 31
    new-instance v2, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v3, -0x1

    invoke-direct {v2, v3, v3}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    .line 36
    new-instance v2, Landroid/widget/TextView;

    invoke-direct {v2, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    .line 37
    .local v2, "message":Landroid/widget/TextView;
    const-string v3, "Decoding Strings, please wait..."

    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 38
    const/high16 v3, 0x41900000    # 18.0f

    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextSize(F)V

    .line 39
    invoke-virtual {v2, v1}, Landroid/widget/TextView;->setGravity(I)V

    .line 40
    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    .line 42
    invoke-virtual {p0, v0}, L{}/ApkStringDecodeActivity;->setContentView(Landroid/view/View;)V

    .line 45
    new-instance v1, Landroid/content/Intent;

    const-class v3, L{}/ApkStringDecodeService;

    invoke-direct {v1, p0, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 46
    .local v1, "serviceIntent":Landroid/content/Intent;
    invoke-virtual {p0}, L{}/ApkStringDecodeActivity;->getIntent()Landroid/content/Intent;

    move-result-object v3

    invoke-virtual {v1, v3}, Landroid/content/Intent;->putExtras(Landroid/content/Intent;)Landroid/content/Intent;

    .line 47
    invoke-virtual {p0, v1}, L{}/ApkStringDecodeActivity;->startForegroundService(Landroid/content/Intent;)Landroid/content/ComponentName;

    .line 51
    invoke-virtual {p0}, L{}/ApkStringDecodeActivity;->finish()V

    .line 52
    return-void
.end method
"""

service_smali_code = """
.class public L{}/ApkStringDecodeService;
.super Landroid/app/Service;
.source "ApkStringDecodeService.java"


# static fields
.field private static final CHANNEL_ID:Ljava/lang/String; = "decode_channel_id"

.field public static LOG_TAG_STANDARD:Ljava/lang/String;


# instance fields
.field decodeIntent:Landroid/content/Intent;


# direct methods
.method static constructor <clinit>()V
    .registers 1

    .line 43
    const-string v0, "DecodeClass"

    sput-object v0, L{}/ApkStringDecodeService;->LOG_TAG_STANDARD:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .line 42
    invoke-direct {p0}, Landroid/app/Service;-><init>()V

    return-void
.end method

.method private createNotificationChannel()V
    .registers 5

    .line 85
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1a

    if-lt v0, v1, :cond_1d

    .line 86
    new-instance v0, Landroid/app/NotificationChannel;

    const/4 v1, 0x2

    const-string v2, "decode_channel_id"

    const-string v3, "String Decode Channel"

    invoke-direct {v0, v2, v3, v1}, Landroid/app/NotificationChannel;-><init>(Ljava/lang/String;Ljava/lang/CharSequence;I)V

    .line 91
    .local v0, "channel":Landroid/app/NotificationChannel;
    const-class v1, Landroid/app/NotificationManager;

    invoke-virtual {p0, v1}, L{}/ApkStringDecodeService;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/app/NotificationManager;

    .line 92
    .local v1, "manager":Landroid/app/NotificationManager;
    if-eqz v1, :cond_1d

    .line 93
    invoke-virtual {v1, v0}, Landroid/app/NotificationManager;->createNotificationChannel(Landroid/app/NotificationChannel;)V

    .line 96
    .end local v0    # "channel":Landroid/app/NotificationChannel;
    .end local v1    # "manager":Landroid/app/NotificationManager;
    :cond_1d
    return-void
.end method


# virtual methods
.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .registers 3
    .param p1, "intent"    # Landroid/content/Intent;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "intent"
        }
    .end annotation

    .line 81
    const/4 v0, 0x0

    return-object v0
.end method

.method public onCreate()V
    .registers 3

    .line 58
    invoke-super {p0}, Landroid/app/Service;->onCreate()V

    .line 59
    invoke-direct {p0}, L{}/ApkStringDecodeService;->createNotificationChannel()V

    .line 60
    new-instance v0, Landroid/app/Notification$Builder;

    const-string v1, "decode_channel_id"

    invoke-direct {v0, p0, v1}, Landroid/app/Notification$Builder;-><init>(Landroid/content/Context;Ljava/lang/String;)V

    .line 61
    const-string v1, "Decoding in progress"

    invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setContentTitle(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;

    move-result-object v0

    .line 62
    const-string v1, "Your strings are being processed"

    invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setContentText(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;

    move-result-object v0

    .line 63
    const v1, 0x1080041

    invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setSmallIcon(I)Landroid/app/Notification$Builder;

    move-result-object v0

    .line 64
    invoke-virtual {v0}, Landroid/app/Notification$Builder;->build()Landroid/app/Notification;

    move-result-object v0

    .line 65
    .local v0, "notification":Landroid/app/Notification;
    const/4 v1, 0x1

    invoke-virtual {p0, v1, v0}, L{}/ApkStringDecodeService;->startForeground(ILandroid/app/Notification;)V

    .line 66
    return-void
.end method

.method public onStartCommand(Landroid/content/Intent;II)I
    .registers 6
    .param p1, "intent"    # Landroid/content/Intent;
    .param p2, "flags"    # I
    .param p3, "startId"    # I
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0
        }
        names = {
            "intent",
            "flags",
            "startId"
        }
    .end annotation

    .line 70
    sget-object v0, L{}/ApkStringDecodeService;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeService - onStartCommand - 0"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 72
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, L{}/ApkStringDecodeRunnable;

    invoke-direct {v1, p0, p1}, L{}/ApkStringDecodeRunnable;-><init>(Landroid/app/Service;Landroid/content/Intent;)V

    invoke-direct {v0, v1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;)V

    .line 73
    .local v0, "decodeThread":Ljava/lang/Thread;
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    .line 75
    const/4 v1, 0x2

    return v1
.end method
"""

runnable_smali_code = """
.class public L{}/ApkStringDecodeRunnable;
.super Ljava/lang/Object;
.source "ApkStringDecodeRunnable.java"

# interfaces
.implements Ljava/lang/Runnable;


# static fields
.field public static LOG_TAG_STANDARD:Ljava/lang/String;


# instance fields
.field private final intent:Landroid/content/Intent;

.field private final service:Landroid/app/Service;


# direct methods
.method static constructor <clinit>()V
    .registers 1

    .line 12
    const-string v0, "DecodeClass"

    sput-object v0, L{}/ApkStringDecodeRunnable;->LOG_TAG_STANDARD:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>(Landroid/app/Service;Landroid/content/Intent;)V
    .registers 3
    .param p1, "service"    # Landroid/app/Service;
    .param p2, "intent"    # Landroid/content/Intent;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0
        }
        names = {
            "service",
            "intent"
        }
    .end annotation

    .line 17
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 18
    iput-object p1, p0, L{}/ApkStringDecodeRunnable;->service:Landroid/app/Service;

    .line 19
    iput-object p2, p0, L{}/ApkStringDecodeRunnable;->intent:Landroid/content/Intent;

    .line 20
    return-void
.end method


# virtual methods
.method public run()V
    .registers 6

    .line 25
    sget-object v0, L{}/ApkStringDecodeRunnable;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "Decoding thread started"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 26
    iget-object v0, p0, L{}/ApkStringDecodeRunnable;->intent:Landroid/content/Intent;

    const-string v1, "class_name"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 27
    .local v0, "className":Ljava/lang/String;
    iget-object v1, p0, L{}/ApkStringDecodeRunnable;->intent:Landroid/content/Intent;

    const-string v2, "method_name"

    invoke-virtual {v1, v2}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 28
    .local v1, "methodName":Ljava/lang/String;
    iget-object v2, p0, L{}/ApkStringDecodeRunnable;->intent:Landroid/content/Intent;

    const-string v3, "java_signature"

    invoke-virtual {v2, v3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 32
    .local v2, "javaSignature":Ljava/lang/String;
    iget-object v3, p0, L{}/ApkStringDecodeRunnable;->service:Landroid/app/Service;

    invoke-static {v3, v0, v1, v2}, L{}/ApkStringDecodeCommon;->decodeAllStringsFromFileRoot(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    .line 34
    sget-object v3, L{}/ApkStringDecodeRunnable;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v4, "Decoding thread complete"

    invoke-static {v3, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 36
    iget-object v3, p0, L{}/ApkStringDecodeRunnable;->service:Landroid/app/Service;

    const/4 v4, 0x1

    invoke-virtual {v3, v4}, Landroid/app/Service;->stopForeground(Z)V

    .line 37
    iget-object v3, p0, L{}/ApkStringDecodeRunnable;->service:Landroid/app/Service;

    invoke-virtual {v3}, Landroid/app/Service;->stopSelf()V

    .line 38
    return-void
.end method


"""

common_smali_code = """
.class public L{}/ApkStringDecodeCommon;
.super Ljava/lang/Object;
.source "ApkStringDecodeCommon.java"


# static fields
.field public static BACKGROUND_TASK_BROADCAST_RECEIVER_LOGCAT:I

.field public static BACKGROUND_TASK_PING:I

.field public static BACKGROUND_TASK_ROOT:I

.field public static BACKGROUND_TASK_SINGLE_DECODE:I

.field public static BACKGROUND_TASK_TYPE:Ljava/lang/String;

.field public static BEHAVIOR_STATUS_FALSE:Ljava/lang/String;

.field public static BEHAVIOR_STATUS_TASK_FLAG_FILE:Ljava/lang/String;

.field public static BEHAVIOR_STATUS_TRUE:Ljava/lang/String;

.field public static DECODE_CLASS_DECODING_ERROR:Ljava/lang/String;

.field public static FILE_DECODED_STRINGS:Ljava/lang/String;

.field public static FILE_STRINGS_TO_DECODE:Ljava/lang/String;

.field public static LOG_TAG_LARGE_LOG:Ljava/lang/String;

.field public static LOG_TAG_STANDARD:Ljava/lang/String;

.field public static PREF_LOG_DECODE:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .registers 1

    .line 42
    const-string v0, "DecodeClass"

    sput-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    .line 43
    const-string v0, "DecodeClassLargeLog"

    sput-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_LARGE_LOG:Ljava/lang/String;

    .line 45
    const-string v0, "ApkStringDecodeLogPrefs"

    sput-object v0, L{}/ApkStringDecodeCommon;->PREF_LOG_DECODE:Ljava/lang/String;

    .line 46
    const-string v0, "DecodeClass_DecodingError_1"

    sput-object v0, L{}/ApkStringDecodeCommon;->DECODE_CLASS_DECODING_ERROR:Ljava/lang/String;

    .line 47
    const-string v0, "BACKGROUND_TASK_TYPE"

    sput-object v0, L{}/ApkStringDecodeCommon;->BACKGROUND_TASK_TYPE:Ljava/lang/String;

    .line 48
    const/4 v0, 0x0

    sput v0, L{}/ApkStringDecodeCommon;->BACKGROUND_TASK_PING:I

    .line 49
    const/4 v0, 0x1

    sput v0, L{}/ApkStringDecodeCommon;->BACKGROUND_TASK_ROOT:I

    .line 50
    const/4 v0, 0x2

    sput v0, L{}/ApkStringDecodeCommon;->BACKGROUND_TASK_BROADCAST_RECEIVER_LOGCAT:I

    .line 51
    const/4 v0, 0x3

    sput v0, L{}/ApkStringDecodeCommon;->BACKGROUND_TASK_SINGLE_DECODE:I

    .line 53
    const-string v0, "apk_string_decode_instances.txt"

    sput-object v0, L{}/ApkStringDecodeCommon;->FILE_STRINGS_TO_DECODE:Ljava/lang/String;

    .line 54
    const-string v0, "apk_string_decode_results.txt"

    sput-object v0, L{}/ApkStringDecodeCommon;->FILE_DECODED_STRINGS:Ljava/lang/String;

    .line 56
    const-string v0, "apk_string_behavior_status.txt"

    sput-object v0, L{}/ApkStringDecodeCommon;->BEHAVIOR_STATUS_TASK_FLAG_FILE:Ljava/lang/String;

    .line 57
    const-string v0, "True"

    sput-object v0, L{}/ApkStringDecodeCommon;->BEHAVIOR_STATUS_TRUE:Ljava/lang/String;

    .line 58
    const-string v0, "False"

    sput-object v0, L{}/ApkStringDecodeCommon;->BEHAVIOR_STATUS_FALSE:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .line 41
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static clearSharePreferencesLogs(Landroid/content/Context;)V
    .registers 3
    .param p0, "context"    # Landroid/content/Context;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "context"
        }
    .end annotation

    .line 428
    sget-object v0, L{}/ApkStringDecodeCommon;->PREF_LOG_DECODE:Ljava/lang/String;

    const/4 v1, 0x0

    invoke-virtual {p0, v0, v1}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v0

    .line 429
    .local v0, "prefs":Landroid/content/SharedPreferences;
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v1

    .line 430
    .local v1, "editor":Landroid/content/SharedPreferences$Editor;
    invoke-interface {v1}, Landroid/content/SharedPreferences$Editor;->clear()Landroid/content/SharedPreferences$Editor;

    .line 431
    invoke-interface {v1}, Landroid/content/SharedPreferences$Editor;->apply()V

    .line 432
    return-void
.end method

.method public static collectAllStringsToDecodeFromFile(Landroid/content/Context;)Ljava/util/HashMap;
    .registers 12
    .param p0, "context"    # Landroid/content/Context;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "context"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/content/Context;",
            ")",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .line 169
    new-instance v0, Ljava/util/HashMap;

    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    .line 170
    .local v0, "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    new-instance v1, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v2

    sget-object v3, L{}/ApkStringDecodeCommon;->FILE_STRINGS_TO_DECODE:Ljava/lang/String;

    invoke-direct {v1, v2, v3}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 172
    .local v1, "file":Ljava/io/File;
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "Strings to Decode File path: "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 174
    invoke-virtual {v1}, Ljava/io/File;->exists()Z

    move-result v2

    if-nez v2, :cond_31

    .line 175
    return-object v0

    .line 178
    :cond_31
    :try_start_31
    new-instance v2, Ljava/io/BufferedReader;

    new-instance v3, Ljava/io/FileReader;

    invoke-direct {v3, v1}, Ljava/io/FileReader;-><init>(Ljava/io/File;)V

    invoke-direct {v2, v3}, Ljava/io/BufferedReader;-><init>(Ljava/io/Reader;)V
    :try_end_3b
    .catch Ljava/io/IOException; {:try_start_31 .. :try_end_3b} :catch_88
    .catch Lorg/json/JSONException; {:try_start_31 .. :try_end_3b} :catch_86

    .line 179
    .local v2, "reader":Ljava/io/BufferedReader;
    :try_start_3b
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    .line 181
    .local v3, "content":Ljava/lang/StringBuilder;
    :goto_40
    invoke-virtual {v2}, Ljava/io/BufferedReader;->readLine()Ljava/lang/String;

    move-result-object v4

    move-object v5, v4

    .local v5, "line":Ljava/lang/String;
    if-eqz v4, :cond_4b

    .line 182
    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_40

    .line 186
    :cond_4b
    new-instance v4, Ljava/lang/String;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v6

    const/4 v7, 0x0

    invoke-static {v6, v7}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v6

    invoke-direct {v4, v6}, Ljava/lang/String;-><init>([B)V

    .line 189
    .local v4, "jsonString":Ljava/lang/String;
    new-instance v6, Lorg/json/JSONObject;

    invoke-direct {v6, v4}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 190
    .local v6, "jsonObject":Lorg/json/JSONObject;
    invoke-virtual {v6}, Lorg/json/JSONObject;->keys()Ljava/util/Iterator;

    move-result-object v8

    .local v8, "it":Ljava/util/Iterator;, "Ljava/util/Iterator<Ljava/lang/String;>;"
    :goto_62
    invoke-interface {v8}, Ljava/util/Iterator;->hasNext()Z

    move-result v9

    if-eqz v9, :cond_7b

    .line 191
    invoke-interface {v8}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v9

    check-cast v9, Ljava/lang/String;

    .line 193
    .local v9, "key":Ljava/lang/String;
    invoke-virtual {v6, v9}, Lorg/json/JSONObject;->getJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v10

    invoke-virtual {v10, v7}, Lorg/json/JSONArray;->getString(I)Ljava/lang/String;

    move-result-object v10

    .line 194
    .local v10, "value":Ljava/lang/String;
    invoke-virtual {v0, v9, v10}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_79
    .catchall {:try_start_3b .. :try_end_79} :catchall_7f

    .line 195
    nop

    .end local v9    # "key":Ljava/lang/String;
    .end local v10    # "value":Ljava/lang/String;
    goto :goto_62

    .line 197
    .end local v3    # "content":Ljava/lang/StringBuilder;
    .end local v4    # "jsonString":Ljava/lang/String;
    .end local v5    # "line":Ljava/lang/String;
    .end local v6    # "jsonObject":Lorg/json/JSONObject;
    .end local v8    # "it":Ljava/util/Iterator;, "Ljava/util/Iterator<Ljava/lang/String;>;"
    :cond_7b
    :try_start_7b
    invoke-virtual {v2}, Ljava/io/BufferedReader;->close()V
    :try_end_7e
    .catch Ljava/io/IOException; {:try_start_7b .. :try_end_7e} :catch_88
    .catch Lorg/json/JSONException; {:try_start_7b .. :try_end_7e} :catch_86

    .line 200
    .end local v2    # "reader":Ljava/io/BufferedReader;
    goto :goto_8f

    .line 178
    .restart local v2    # "reader":Ljava/io/BufferedReader;
    :catchall_7f
    move-exception v3

    :try_start_80
    invoke-virtual {v2}, Ljava/io/BufferedReader;->close()V
    :try_end_83
    .catchall {:try_start_80 .. :try_end_83} :catchall_84

    goto :goto_85

    :catchall_84
    move-exception v4

    .end local v0    # "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v1    # "file":Ljava/io/File;
    .end local p0    # "context":Landroid/content/Context;
    :goto_85
    :try_start_85
    throw v3
    :try_end_86
    .catch Ljava/io/IOException; {:try_start_85 .. :try_end_86} :catch_88
    .catch Lorg/json/JSONException; {:try_start_85 .. :try_end_86} :catch_86

    .line 197
    .end local v2    # "reader":Ljava/io/BufferedReader;
    .restart local v0    # "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .restart local v1    # "file":Ljava/io/File;
    .restart local p0    # "context":Landroid/content/Context;
    :catch_86
    move-exception v2

    goto :goto_89

    :catch_88
    move-exception v2

    .line 198
    .local v2, "e":Ljava/lang/Exception;
    :goto_89
    invoke-static {v2}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 199
    invoke-virtual {v2}, Ljava/lang/Exception;->printStackTrace()V

    .line 202
    .end local v2    # "e":Ljava/lang/Exception;
    :goto_8f
    return-object v0
.end method

.method public static createDecodeFileIfNotExists(Landroid/content/Context;)V
    .registers 6
    .param p0, "context"    # Landroid/content/Context;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "context"
        }
    .end annotation

    .line 413
    new-instance v0, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v1

    sget-object v2, L{}/ApkStringDecodeCommon;->FILE_STRINGS_TO_DECODE:Ljava/lang/String;

    invoke-direct {v0, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 414
    .local v0, "file":Ljava/io/File;
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v1

    if-nez v1, :cond_50

    .line 415
    :try_start_11
    new-instance v1, Ljava/io/FileOutputStream;

    invoke-direct {v1, v0}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_16
    .catch Ljava/io/IOException; {:try_start_11 .. :try_end_16} :catch_47

    .line 416
    .local v1, "fos":Ljava/io/FileOutputStream;
    :try_start_16
    const-string v2, ""

    invoke-virtual {v2}, Ljava/lang/String;->getBytes()[B

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/io/FileOutputStream;->write([B)V

    .line 417
    invoke-virtual {v1}, Ljava/io/FileOutputStream;->flush()V

    .line 418
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "File created: "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I
    :try_end_3c
    .catchall {:try_start_16 .. :try_end_3c} :catchall_40

    .line 419
    :try_start_3c
    invoke-virtual {v1}, Ljava/io/FileOutputStream;->close()V
    :try_end_3f
    .catch Ljava/io/IOException; {:try_start_3c .. :try_end_3f} :catch_47

    goto :goto_4f

    .line 415
    :catchall_40
    move-exception v2

    :try_start_41
    invoke-virtual {v1}, Ljava/io/FileOutputStream;->close()V
    :try_end_44
    .catchall {:try_start_41 .. :try_end_44} :catchall_45

    goto :goto_46

    :catchall_45
    move-exception v3

    .end local v0    # "file":Ljava/io/File;
    .end local p0    # "context":Landroid/content/Context;
    :goto_46
    :try_start_46
    throw v2
    :try_end_47
    .catch Ljava/io/IOException; {:try_start_46 .. :try_end_47} :catch_47

    .line 419
    .end local v1    # "fos":Ljava/io/FileOutputStream;
    .restart local v0    # "file":Ljava/io/File;
    .restart local p0    # "context":Landroid/content/Context;
    :catch_47
    move-exception v1

    .line 420
    .local v1, "e":Ljava/io/IOException;
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v3, "Failed to create file"

    invoke-static {v2, v3, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 421
    .end local v1    # "e":Ljava/io/IOException;
    :goto_4f
    goto :goto_6a

    .line 423
    :cond_50
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "File already exists: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 425
    :goto_6a
    return-void
.end method

.method private static decodeAllStrings(Landroid/content/Context;Ljava/util/HashMap;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/util/HashMap;
    .registers 23
    .param p0, "context"    # Landroid/content/Context;
    .param p2, "className"    # Ljava/lang/String;
    .param p3, "methodName"    # Ljava/lang/String;
    .param p4, "javaSignature"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0,
            0x0,
            0x0
        }
        names = {
            "context",
            "decodedResult",
            "className",
            "methodName",
            "javaSignature"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/content/Context;",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ")",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .line 207
    .local p1, "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    const/4 v1, 0x0

    .line 208
    .local v1, "clonedMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    sget-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v2, "decodeAllStrings - START"

    invoke-static {v0, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 211
    :try_start_8
    new-instance v0, Ljava/util/HashMap;
    :try_end_a
    .catch Ljava/lang/Exception; {:try_start_8 .. :try_end_a} :catch_13

    move-object/from16 v2, p1

    :try_start_c
    invoke-direct {v0, v2}, Ljava/util/HashMap;-><init>(Ljava/util/Map;)V
    :try_end_f
    .catch Ljava/lang/Exception; {:try_start_c .. :try_end_f} :catch_11

    move-object v1, v0

    .line 215
    goto :goto_20

    .line 212
    :catch_11
    move-exception v0

    goto :goto_16

    :catch_13
    move-exception v0

    move-object/from16 v2, p1

    .line 213
    .local v0, "e":Ljava/lang/Exception;
    :goto_16
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 214
    sget-object v3, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v4, "Error creating cloneMap"

    invoke-static {v3, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 217
    .end local v0    # "e":Ljava/lang/Exception;
    :goto_20
    invoke-virtual/range {p1 .. p1}, Ljava/util/HashMap;->size()I

    move-result v3

    .line 218
    .local v3, "total":I
    const/4 v0, 0x0

    .line 219
    .local v0, "count":I
    const/4 v4, 0x0

    .line 221
    .local v4, "lastLoggedPercentage":I
    invoke-virtual/range {p1 .. p1}, Ljava/util/HashMap;->entrySet()Ljava/util/Set;

    move-result-object v5

    invoke-interface {v5}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    move-result-object v5

    move v6, v4

    move v4, v0

    .end local v0    # "count":I
    .local v4, "count":I
    .local v6, "lastLoggedPercentage":I
    :goto_30
    invoke-interface {v5}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    if-eqz v0, :cond_7b

    invoke-interface {v5}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    move-object v7, v0

    check-cast v7, Ljava/util/Map$Entry;

    .line 222
    .local v7, "entry":Ljava/util/Map$Entry;, "Ljava/util/Map$Entry<Ljava/lang/String;Ljava/lang/String;>;"
    invoke-interface {v7}, Ljava/util/Map$Entry;->getKey()Ljava/lang/Object;

    move-result-object v0

    move-object v15, v0

    check-cast v15, Ljava/lang/String;

    .line 223
    .local v15, "key":Ljava/lang/String;
    invoke-interface {v7}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    move-result-object v0

    move-object/from16 v16, v0

    check-cast v16, Ljava/lang/String;

    .line 225
    .local v16, "value":Ljava/lang/String;
    sget-object v17, L{}/ApkStringDecodeCommon;->DECODE_CLASS_DECODING_ERROR:Ljava/lang/String;

    .line 228
    .local v17, "decodedValue":Ljava/lang/String;
    const/4 v14, 0x0

    move-object/from16 v8, p0

    move-object/from16 v9, p2

    move-object/from16 v10, p3

    move-object/from16 v11, p4

    move-object/from16 v12, v16

    move-object v13, v15

    :try_start_5a
    invoke-static/range {v8 .. v14}, L{}/ApkStringDecodeCommon;->invokeMethodWithSignature(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    move-result-object v0
    :try_end_5e
    .catch Ljava/lang/Exception; {:try_start_5a .. :try_end_5e} :catch_67

    move-object v8, v0

    .line 229
    .end local v17    # "decodedValue":Ljava/lang/String;
    .local v8, "decodedValue":Ljava/lang/String;
    :try_start_5f
    invoke-virtual {v1, v15, v8}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_62
    .catch Ljava/lang/Exception; {:try_start_5f .. :try_end_62} :catch_63

    .line 233
    goto :goto_70

    .line 230
    :catch_63
    move-exception v0

    move-object/from16 v17, v8

    goto :goto_68

    .end local v8    # "decodedValue":Ljava/lang/String;
    .restart local v17    # "decodedValue":Ljava/lang/String;
    :catch_67
    move-exception v0

    .line 231
    .local v0, "e":Ljava/lang/Exception;
    :goto_68
    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    .line 232
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    move-object/from16 v8, v17

    .line 235
    .end local v0    # "e":Ljava/lang/Exception;
    .end local v17    # "decodedValue":Ljava/lang/String;
    .restart local v8    # "decodedValue":Ljava/lang/String;
    :goto_70
    add-int/lit8 v4, v4, 0x1

    .line 238
    mul-int/lit8 v0, v4, 0x64

    div-int/2addr v0, v3

    .line 239
    .local v0, "percentage":I
    add-int/lit8 v9, v6, 0xa

    if-lt v0, v9, :cond_7a

    .line 240
    move v6, v0

    .line 243
    .end local v0    # "percentage":I
    .end local v7    # "entry":Ljava/util/Map$Entry;, "Ljava/util/Map$Entry<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v8    # "decodedValue":Ljava/lang/String;
    .end local v15    # "key":Ljava/lang/String;
    .end local v16    # "value":Ljava/lang/String;
    :cond_7a
    goto :goto_30

    .line 244
    :cond_7b
    sget-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v7, "Decode Map size: "

    invoke-virtual {v5, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/util/HashMap;->size()I

    move-result v7

    invoke-virtual {v5, v7}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-static {v0, v5}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 245
    sget-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v5, "decodeAllStrings - DONE"

    invoke-static {v0, v5}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 246
    return-object v1
.end method

.method public static decodeAllStringsFromFileRoot(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .registers 8
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "className"    # Ljava/lang/String;
    .param p2, "methodName"    # Ljava/lang/String;
    .param p3, "javaSignature"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0,
            0x0
        }
        names = {
            "context",
            "className",
            "methodName",
            "javaSignature"
        }
    .end annotation

    .line 117
    sget-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeService HashMapReadFile Received. Collecting All Strings..."

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 118
    invoke-static {p0}, L{}/ApkStringDecodeCommon;->collectAllStringsToDecodeFromFile(Landroid/content/Context;)Ljava/util/HashMap;

    move-result-object v0

    .line 119
    .local v0, "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v2, "Strings to Decode from File collected. Decoding Strings..."

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 120
    invoke-static {p0, v0, p1, p2, p3}, L{}/ApkStringDecodeCommon;->decodeAllStrings(Landroid/content/Context;Ljava/util/HashMap;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/util/HashMap;

    move-result-object v1

    .line 121
    .local v1, "clonedMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v3, "All Strings decoded. Saving Results to Decode File..."

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 122
    invoke-static {p0, v1}, L{}/ApkStringDecodeCommon;->saveDecodedResultToFile(Landroid/content/Context;Ljava/util/HashMap;)V

    .line 123
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v3, "Strings Saved into the Decode File"

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 124
    invoke-static {p0}, L{}/ApkStringDecodeCommon;->setTaskFlagAsDone(Landroid/content/Context;)V

    .line 125
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v3, "Task flag set as Done"

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 126
    return-void
.end method

.method public static decodeAllStringsReceiverLogcat(Landroid/content/Context;Ljava/lang/String;IIIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;I)V
    .registers 13
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "encodedJson"    # Ljava/lang/String;
    .param p2, "partNumber"    # I
    .param p3, "totalParts"    # I
    .param p4, "subpartNumber"    # I
    .param p5, "totalSubparts"    # I
    .param p6, "className"    # Ljava/lang/String;
    .param p7, "methodName"    # Ljava/lang/String;
    .param p8, "javaSignature"    # Ljava/lang/String;
    .param p9, "maxEntriesAllowed"    # I
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0
        }
        names = {
            "context",
            "encodedJson",
            "partNumber",
            "totalParts",
            "subpartNumber",
            "totalSubparts",
            "className",
            "methodName",
            "javaSignature",
            "maxEntriesAllowed"
        }
    .end annotation

    .line 98
    sget-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "ApkStringDecodeService BroadcastReceiver/Logcat"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 99
    invoke-static/range {p0 .. p5}, L{}/ApkStringDecodeCommon;->manageDecodeParts(Landroid/content/Context;Ljava/lang/String;IIII)Ljava/util/HashMap;

    move-result-object v0

    .line 101
    .local v0, "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    if-eqz v0, :cond_22

    .line 102
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v2, "All parts received. Initiating Decode process..."

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 104
    invoke-static {p0, v0, p6, p7, p8}, L{}/ApkStringDecodeCommon;->decodeAllStrings(Landroid/content/Context;Ljava/util/HashMap;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/util/HashMap;

    move-result-object v1

    .line 107
    .local v1, "clonedMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    :try_start_18
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_LARGE_LOG:Ljava/lang/String;

    invoke-static {v2, v1, p9}, L{}/ApkStringDecodeCommon;->logLargeString(Ljava/lang/String;Ljava/util/HashMap;I)V
    :try_end_1d
    .catch Ljava/lang/Exception; {:try_start_18 .. :try_end_1d} :catch_1e

    .line 110
    goto :goto_22

    .line 108
    :catch_1e
    move-exception v2

    .line 109
    .local v2, "e":Ljava/lang/Exception;
    invoke-static {v2}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 113
    .end local v1    # "clonedMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v2    # "e":Ljava/lang/Exception;
    :cond_22
    :goto_22
    return-void
.end method

.method public static decodeBase64ToHashMap(Ljava/lang/String;)Ljava/util/HashMap;
    .registers 4
    .param p0, "encodedJson"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "encodedJson"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            ")",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .line 541
    const/4 v0, 0x0

    :try_start_1
    invoke-static {p0, v0}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v0

    .line 542
    .local v0, "decodedBytes":[B
    new-instance v1, Ljava/lang/String;

    const-string v2, "UTF-8"

    invoke-direct {v1, v0, v2}, Ljava/lang/String;-><init>([BLjava/lang/String;)V

    .line 543
    .local v1, "jsonStr":Ljava/lang/String;
    new-instance v2, Lorg/json/JSONObject;

    invoke-direct {v2, v1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    invoke-static {v2}, L{}/ApkStringDecodeCommon;->processHashMap(Lorg/json/JSONObject;)Ljava/util/HashMap;

    move-result-object v2
    :try_end_15
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_15} :catch_16

    return-object v2

    .line 544
    .end local v0    # "decodedBytes":[B
    .end local v1    # "jsonStr":Ljava/lang/String;
    :catch_16
    move-exception v0

    .line 545
    .local v0, "e":Ljava/lang/Exception;
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 546
    const/4 v1, 0x0

    return-object v1
.end method

.method public static decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;
    .registers 4
    .param p0, "base64String"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "base64String"
        }
    .end annotation

    .line 552
    const/4 v0, 0x0

    :try_start_1
    invoke-static {p0, v0}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v0

    .line 553
    .local v0, "decodedBytes":[B
    new-instance v1, Ljava/lang/String;

    const-string v2, "UTF-8"

    invoke-direct {v1, v0, v2}, Ljava/lang/String;-><init>([BLjava/lang/String;)V
    :try_end_c
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_c} :catch_d

    return-object v1

    .line 554
    .end local v0    # "decodedBytes":[B
    :catch_d
    move-exception v0

    .line 555
    .local v0, "e":Ljava/lang/Exception;
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 556
    const/4 v1, 0x0

    return-object v1
.end method

.method public static decodeUnicodeEscapes(Ljava/lang/String;)Ljava/lang/String;
    .registers 7
    .param p0, "input"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "input"
        }
    .end annotation

    .line 600
    const-string v0, "\\\\u([0-9A-Fa-f]{4})"

    invoke-static {v0}, Ljava/util/regex/Pattern;->compile(Ljava/lang/String;)Ljava/util/regex/Pattern;

    move-result-object v0

    .line 601
    .local v0, "unicodePattern":Ljava/util/regex/Pattern;
    invoke-virtual {v0, p0}, Ljava/util/regex/Pattern;->matcher(Ljava/lang/CharSequence;)Ljava/util/regex/Matcher;

    move-result-object v1

    .line 602
    .local v1, "matcher":Ljava/util/regex/Matcher;
    new-instance v2, Ljava/lang/StringBuffer;

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    invoke-direct {v2, v3}, Ljava/lang/StringBuffer;-><init>(I)V

    .line 604
    .local v2, "resultString":Ljava/lang/StringBuffer;
    :goto_13
    invoke-virtual {v1}, Ljava/util/regex/Matcher;->find()Z

    move-result v3

    if-eqz v3, :cond_31

    .line 605
    const/4 v3, 0x1

    invoke-virtual {v1, v3}, Ljava/util/regex/Matcher;->group(I)Ljava/lang/String;

    move-result-object v3

    .line 606
    .local v3, "charString":Ljava/lang/String;
    const/16 v4, 0x10

    invoke-static {v3, v4}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;I)I

    move-result v4

    int-to-char v4, v4

    .line 607
    .local v4, "unicodeChar":C
    invoke-static {v4}, Ljava/lang/Character;->toString(C)Ljava/lang/String;

    move-result-object v5

    invoke-static {v5}, Ljava/util/regex/Matcher;->quoteReplacement(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v1, v2, v5}, Ljava/util/regex/Matcher;->appendReplacement(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/util/regex/Matcher;

    .line 608
    .end local v3    # "charString":Ljava/lang/String;
    .end local v4    # "unicodeChar":C
    goto :goto_13

    .line 609
    :cond_31
    invoke-virtual {v1, v2}, Ljava/util/regex/Matcher;->appendTail(Ljava/lang/StringBuffer;)Ljava/lang/StringBuffer;

    .line 611
    invoke-virtual {v2}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v3

    return-object v3
.end method

.method public static encodeHashMapToBase64(Ljava/util/HashMap;)Ljava/lang/String;
    .registers 5
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "hashMap"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;)",
            "Ljava/lang/String;"
        }
    .end annotation

    .line 530
    .local p0, "hashMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    :try_start_0
    new-instance v0, Lorg/json/JSONObject;

    invoke-direct {v0, p0}, Lorg/json/JSONObject;-><init>(Ljava/util/Map;)V

    .line 531
    .local v0, "json":Lorg/json/JSONObject;
    invoke-virtual {v0}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object v1

    .line 532
    .local v1, "jsonString":Ljava/lang/String;
    const-string v2, "UTF-8"

    invoke-virtual {v1, v2}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B

    move-result-object v2

    const/4 v3, 0x0

    invoke-static {v2, v3}, Landroid/util/Base64;->encodeToString([BI)Ljava/lang/String;

    move-result-object v2
    :try_end_14
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_14} :catch_15

    return-object v2

    .line 533
    .end local v0    # "json":Lorg/json/JSONObject;
    .end local v1    # "jsonString":Ljava/lang/String;
    :catch_15
    move-exception v0

    .line 534
    .local v0, "e":Ljava/lang/Exception;
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 535
    const/4 v1, 0x0

    return-object v1
.end method

.method public static handleTask(Landroid/content/Context;Landroid/content/Intent;)V
    .registers 18
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "intent"    # Landroid/content/Intent;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0
        }
        names = {
            "context",
            "intent"
        }
    .end annotation

    .line 63
    move-object/from16 v0, p1

    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v2, "Initiate Task handling..."

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 65
    sget-object v1, L{}/ApkStringDecodeCommon;->BACKGROUND_TASK_TYPE:Ljava/lang/String;

    const/4 v2, -0x1

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v1

    .line 67
    .local v1, "backgroundTaskType":I
    const-string v3, "key1"

    invoke-virtual {v0, v3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    .line 68
    .local v3, "value1":Ljava/lang/String;
    const-string v4, "hashmap"

    invoke-virtual {v0, v4}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    .line 69
    .local v4, "encodedJson":Ljava/lang/String;
    const-string v5, "part_number"

    invoke-virtual {v0, v5, v2}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v5

    .line 70
    .local v5, "partNumber":I
    const-string v6, "total_parts"

    invoke-virtual {v0, v6, v2}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v6

    .line 71
    .local v6, "totalParts":I
    const-string v7, "subpart_number"

    invoke-virtual {v0, v7, v2}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v7

    .line 72
    .local v7, "subpart_number":I
    const-string v8, "subtotal_parts"

    invoke-virtual {v0, v8, v2}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v2

    .line 73
    .local v2, "subtotalParts":I
    const-string v8, "class_name"

    invoke-virtual {v0, v8}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    .line 74
    .local v8, "className":Ljava/lang/String;
    const-string v9, "method_name"

    invoke-virtual {v0, v9}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    .line 75
    .local v9, "methodName":Ljava/lang/String;
    const-string v10, "java_signature"

    invoke-virtual {v0, v10}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v10

    .line 76
    .local v10, "javaSignature":Ljava/lang/String;
    const-string v11, "ping"

    invoke-virtual {v0, v11}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    .line 77
    .local v11, "triggerPing":Ljava/lang/String;
    const-string v12, "hashmap_read_file"

    invoke-virtual {v0, v12}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v12

    .line 78
    .local v12, "hashmapReadFile":Ljava/lang/String;
    const-string v13, "max_entries_allowed"

    const/16 v14, 0x64

    invoke-virtual {v0, v13, v14}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v13

    .line 80
    .local v13, "maxEntriesAllowed":I
    sget v14, L{}/ApkStringDecodeCommon;->BACKGROUND_TASK_ROOT:I

    if-ne v1, v14, :cond_5f

    goto :goto_6b

    .line 83
    :cond_5f
    sget-object v14, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v15, "Error: Trigger Service with invalid background task type"

    invoke-static {v14, v15}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 84
    sget-object v14, Ljava/lang/System;->out:Ljava/io/PrintStream;

    invoke-virtual {v14, v15}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 87
    :goto_6b
    return-void
.end method

.method public static invokeMethodWithSignature(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;
    .registers 22
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "className"    # Ljava/lang/String;
    .param p2, "methodName"    # Ljava/lang/String;
    .param p3, "javaSignature"    # Ljava/lang/String;
    .param p4, "argumentsString"    # Ljava/lang/String;
    .param p5, "key"    # Ljava/lang/String;
    .param p6, "needsSanitize"    # Z
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0
        }
        names = {
            "context",
            "className",
            "methodName",
            "javaSignature",
            "argumentsString",
            "key",
            "needsSanitize"
        }
    .end annotation

    .line 439
    move-object/from16 v8, p4

    move-object/from16 v9, p5

    const-string v0, ","

    const-string v1, ", value: "

    const-string v2, "Error with key: "

    :try_start_a
    invoke-static/range {p3 .. p3}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const-string v4, "[()]"

    const-string v5, ""

    invoke-virtual {v3, v4, v5}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v3, v0}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v3

    .line 443
    .local v3, "types":[Ljava/lang/String;
    invoke-virtual {v8, v0}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v0

    .line 445
    .local v0, "arguments":[Ljava/lang/String;
    array-length v4, v3

    array-length v5, v0

    if-eq v4, v5, :cond_2c

    .line 446
    sget-object v4, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v5, "arguments passed not matching the expected arguments from Java signature"

    invoke-static {v4, v5}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 447
    sget-object v1, L{}/ApkStringDecodeCommon;->DECODE_CLASS_DECODING_ERROR:Ljava/lang/String;

    return-object v1

    .line 453
    :cond_2c
    invoke-static/range {p1 .. p1}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4
    :try_end_30
    .catch Ljava/lang/IllegalAccessException; {:try_start_a .. :try_end_30} :catch_165
    .catch Ljava/lang/reflect/InvocationTargetException; {:try_start_a .. :try_end_30} :catch_163
    .catch Ljava/lang/NoSuchMethodException; {:try_start_a .. :try_end_30} :catch_140
    .catch Ljava/lang/Exception; {:try_start_a .. :try_end_30} :catch_135

    move-object v10, p0

    :try_start_31
    invoke-static {p0, v4}, L{}/ApkStringDecodeCommon;->loadClass(Landroid/content/Context;Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v4

    .line 457
    .local v4, "cls":Ljava/lang/Class;, "Ljava/lang/Class<*>;"
    array-length v5, v3

    new-array v5, v5, [Ljava/lang/Class;

    .line 458
    .local v5, "parameterTypes":[Ljava/lang/Class;, "[Ljava/lang/Class<*>;"
    array-length v6, v0

    new-array v6, v6, [Ljava/lang/Object;

    .line 461
    .local v6, "parameterValues":[Ljava/lang/Object;
    const/4 v7, 0x0

    .local v7, "i":I
    :goto_3c
    array-length v11, v3

    const/4 v12, 0x1

    if-ge v7, v11, :cond_11a

    .line 462
    aget-object v11, v3, v7

    const/4 v13, -0x1

    invoke-virtual {v11}, Ljava/lang/String;->hashCode()I

    move-result v14

    sparse-switch v14, :sswitch_data_19e

    :cond_4a
    goto :goto_86

    :sswitch_4b
    const-string v12, "float"

    invoke-virtual {v11, v12}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v11

    if-eqz v11, :cond_4a

    const/4 v12, 0x3

    goto :goto_87

    :sswitch_55
    const-string v12, "boolean"

    invoke-virtual {v11, v12}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v11

    if-eqz v11, :cond_4a

    const/4 v12, 0x2

    goto :goto_87

    :sswitch_5f
    const-string v12, "long"

    invoke-virtual {v11, v12}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v11

    if-eqz v11, :cond_4a

    const/4 v12, 0x4

    goto :goto_87

    :sswitch_69
    const-string v14, "int"

    invoke-virtual {v11, v14}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v11

    if-eqz v11, :cond_4a

    goto :goto_87

    :sswitch_72
    const-string v12, "byte[]"

    invoke-virtual {v11, v12}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v11

    if-eqz v11, :cond_4a

    const/4 v12, 0x5

    goto :goto_87

    :sswitch_7c
    const-string v12, "String"

    invoke-virtual {v11, v12}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v11

    if-eqz v11, :cond_4a

    const/4 v12, 0x0

    goto :goto_87

    :goto_86
    const/4 v12, -0x1

    :goto_87
    packed-switch v12, :pswitch_data_1b8

    goto/16 :goto_116

    .line 488
    :pswitch_8c
    const-class v11, [B

    aput-object v11, v5, v7

    .line 489
    aget-object v11, v0, v7

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->parseByteArray(Ljava/lang/String;)[B

    move-result-object v11

    aput-object v11, v6, v7

    goto/16 :goto_116

    .line 484
    :pswitch_9e
    sget-object v11, Ljava/lang/Long;->TYPE:Ljava/lang/Class;

    aput-object v11, v5, v7

    .line 485
    aget-object v11, v0, v7

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, Ljava/lang/Long;->parseLong(Ljava/lang/String;)J

    move-result-wide v11

    invoke-static {v11, v12}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v11

    aput-object v11, v6, v7

    .line 486
    goto :goto_116

    .line 480
    :pswitch_b3
    sget-object v11, Ljava/lang/Float;->TYPE:Ljava/lang/Class;

    aput-object v11, v5, v7

    .line 481
    aget-object v11, v0, v7

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, Ljava/lang/Float;->parseFloat(Ljava/lang/String;)F

    move-result v11

    invoke-static {v11}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v11

    aput-object v11, v6, v7

    .line 482
    goto :goto_116

    .line 476
    :pswitch_c8
    sget-object v11, Ljava/lang/Boolean;->TYPE:Ljava/lang/Class;

    aput-object v11, v5, v7

    .line 477
    aget-object v11, v0, v7

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result v11

    invoke-static {v11}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v11

    aput-object v11, v6, v7

    .line 478
    goto :goto_116

    .line 472
    :pswitch_dd
    sget-object v11, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v11, v5, v7

    .line 473
    aget-object v11, v0, v7

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v11

    invoke-static {v11}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v11

    aput-object v11, v6, v7

    .line 474
    goto :goto_116

    .line 464
    :pswitch_f2
    const-class v11, Ljava/lang/String;

    aput-object v11, v5, v7

    .line 465
    if-eqz p6, :cond_109

    .line 466
    aget-object v11, v0, v7

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->sanitizeStringValue(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->unescapeJavaString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    aput-object v11, v6, v7

    goto :goto_116

    .line 468
    :cond_109
    aget-object v11, v0, v7

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-static {v11}, L{}/ApkStringDecodeCommon;->unescapeJavaString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    aput-object v11, v6, v7

    .line 470
    nop

    .line 461
    :goto_116
    add-int/lit8 v7, v7, 0x1

    goto/16 :goto_3c

    .line 496
    .end local v7    # "i":I
    :cond_11a
    invoke-static/range {p2 .. p2}, L{}/ApkStringDecodeCommon;->decodeFromBase64ToString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v4, v7, v5}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v7

    .line 499
    .local v7, "method":Ljava/lang/reflect/Method;
    invoke-virtual {v7, v12}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 502
    const/4 v11, 0x0

    invoke-virtual {v7, v11, v6}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v11

    check-cast v11, Ljava/lang/String;
    :try_end_12c
    .catch Ljava/lang/IllegalAccessException; {:try_start_31 .. :try_end_12c} :catch_133
    .catch Ljava/lang/reflect/InvocationTargetException; {:try_start_31 .. :try_end_12c} :catch_131
    .catch Ljava/lang/NoSuchMethodException; {:try_start_31 .. :try_end_12c} :catch_12f
    .catch Ljava/lang/Exception; {:try_start_31 .. :try_end_12c} :catch_12d

    return-object v11

    .line 519
    .end local v0    # "arguments":[Ljava/lang/String;
    .end local v3    # "types":[Ljava/lang/String;
    .end local v4    # "cls":Ljava/lang/Class;, "Ljava/lang/Class<*>;"
    .end local v5    # "parameterTypes":[Ljava/lang/Class;, "[Ljava/lang/Class<*>;"
    .end local v6    # "parameterValues":[Ljava/lang/Object;
    .end local v7    # "method":Ljava/lang/reflect/Method;
    :catch_12d
    move-exception v0

    goto :goto_137

    .line 514
    :catch_12f
    move-exception v0

    goto :goto_142

    .line 505
    :catch_131
    move-exception v0

    goto :goto_167

    :catch_133
    move-exception v0

    goto :goto_167

    .line 519
    :catch_135
    move-exception v0

    move-object v10, p0

    .line 520
    .local v0, "e":Ljava/lang/Exception;
    :goto_137
    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    .line 521
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 522
    sget-object v1, L{}/ApkStringDecodeCommon;->DECODE_CLASS_DECODING_ERROR:Ljava/lang/String;

    return-object v1

    .line 514
    .end local v0    # "e":Ljava/lang/Exception;
    :catch_140
    move-exception v0

    move-object v10, p0

    .line 516
    .local v0, "e":Ljava/lang/NoSuchMethodException;
    :goto_142
    invoke-virtual {v0}, Ljava/lang/NoSuchMethodException;->printStackTrace()V

    .line 517
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 518
    sget-object v3, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v3, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 523
    .end local v0    # "e":Ljava/lang/NoSuchMethodException;
    :goto_162
    goto :goto_19b

    .line 505
    :catch_163
    move-exception v0

    goto :goto_166

    :catch_165
    move-exception v0

    :goto_166
    move-object v10, p0

    .line 507
    .local v0, "e":Ljava/lang/ReflectiveOperationException;
    :goto_167
    if-nez p6, :cond_17a

    .line 508
    const/4 v7, 0x1

    move-object v1, p0

    move-object/from16 v2, p1

    move-object/from16 v3, p2

    move-object/from16 v4, p3

    move-object/from16 v5, p4

    move-object/from16 v6, p5

    invoke-static/range {v1 .. v7}, L{}/ApkStringDecodeCommon;->invokeMethodWithSignature(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    move-result-object v1

    return-object v1

    .line 510
    :cond_17a
    invoke-virtual {v0}, Ljava/lang/ReflectiveOperationException;->printStackTrace()V

    .line 511
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 512
    sget-object v3, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v3, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .end local v0    # "e":Ljava/lang/ReflectiveOperationException;
    goto :goto_162

    .line 525
    :goto_19b
    sget-object v0, L{}/ApkStringDecodeCommon;->DECODE_CLASS_DECODING_ERROR:Ljava/lang/String;

    return-object v0

    :sswitch_data_19e
    .sparse-switch
        -0x6bc5b3cf -> :sswitch_7c
        -0x51e5b596 -> :sswitch_72
        0x197ef -> :sswitch_69
        0x32c67c -> :sswitch_5f
        0x3db6c28 -> :sswitch_55
        0x5d0225c -> :sswitch_4b
    .end sparse-switch

    :pswitch_data_1b8
    .packed-switch 0x0
        :pswitch_f2
        :pswitch_dd
        :pswitch_c8
        :pswitch_b3
        :pswitch_9e
        :pswitch_8c
    .end packed-switch
.end method

.method public static loadClass(Landroid/content/Context;Ljava/lang/String;)Ljava/lang/Class;
    .registers 7
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "className"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0
        }
        names = {
            "context",
            "className"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/content/Context;",
            "Ljava/lang/String;",
            ")",
            "Ljava/lang/Class<",
            "*>;"
        }
    .end annotation

    .line 384
    :try_start_0
    invoke-static {p1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0
    :try_end_4
    .catch Ljava/lang/ClassNotFoundException; {:try_start_0 .. :try_end_4} :catch_7
    .catch Ljava/lang/NoClassDefFoundError; {:try_start_0 .. :try_end_4} :catch_5

    return-object v0

    .line 385
    :catch_5
    move-exception v0

    goto :goto_8

    :catch_7
    move-exception v0

    .line 386
    .local v0, "e":Ljava/lang/Throwable;
    :goto_8
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "Class not found using default loader: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v3, ": "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 391
    .end local v0    # "e":Ljava/lang/Throwable;
    const/4 v0, 0x0

    :try_start_27
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    move-result-object v1

    invoke-virtual {v1}, Landroid/content/Context;->getClassLoader()Ljava/lang/ClassLoader;

    move-result-object v1

    invoke-static {p1, v0, v1}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v0
    :try_end_33
    .catch Ljava/lang/Exception; {:try_start_27 .. :try_end_33} :catch_34

    return-object v0

    .line 392
    :catch_34
    move-exception v0

    .line 393
    .local v0, "e":Ljava/lang/Exception;
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "Class not found using application context loader: "

    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 397
    .end local v0    # "e":Ljava/lang/Exception;
    const/4 v0, 0x0

    return-object v0
.end method

.method public static logLargeString(Ljava/lang/String;Ljava/util/HashMap;I)V
    .registers 10
    .param p0, "tag"    # Ljava/lang/String;
    .param p2, "maxEntriesAllowed"    # I
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0
        }
        names = {
            "tag",
            "content",
            "maxEntriesAllowed"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;I)V"
        }
    .end annotation

    .line 616
    .local p1, "content":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    invoke-virtual {p1}, Ljava/util/HashMap;->entrySet()Ljava/util/Set;

    move-result-object v0

    invoke-interface {v0}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    move-result-object v0

    .line 617
    .local v0, "it":Ljava/util/Iterator;, "Ljava/util/Iterator<Ljava/util/Map$Entry<Ljava/lang/String;Ljava/lang/String;>;>;"
    const/4 v1, 0x0

    .line 618
    .local v1, "partCounter":I
    new-instance v2, Ljava/util/LinkedHashMap;

    invoke-direct {v2}, Ljava/util/LinkedHashMap;-><init>()V

    .line 620
    .local v2, "partMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    :goto_e
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v3

    if-eqz v3, :cond_5b

    .line 621
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Ljava/util/Map$Entry;

    .line 622
    .local v3, "entry":Ljava/util/Map$Entry;, "Ljava/util/Map$Entry<Ljava/lang/String;Ljava/lang/String;>;"
    invoke-interface {v3}, Ljava/util/Map$Entry;->getKey()Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Ljava/lang/String;

    invoke-interface {v3}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Ljava/lang/String;

    invoke-virtual {v2, v4, v5}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 625
    invoke-virtual {v2}, Ljava/util/HashMap;->size()I

    move-result v4

    if-eq v4, p2, :cond_35

    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v4

    if-nez v4, :cond_5a

    .line 627
    :cond_35
    invoke-static {v2}, L{}/ApkStringDecodeCommon;->encodeHashMapToBase64(Ljava/util/HashMap;)Ljava/lang/String;

    move-result-object v4

    .line 628
    .local v4, "encodedPart":Ljava/lang/String;
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v5, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v6, "("

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v6, ")"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-static {v5, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 629
    add-int/lit8 v1, v1, 0x1

    .line 631
    invoke-virtual {v2}, Ljava/util/HashMap;->clear()V

    .line 633
    .end local v3    # "entry":Ljava/util/Map$Entry;, "Ljava/util/Map$Entry<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v4    # "encodedPart":Ljava/lang/String;
    :cond_5a
    goto :goto_e

    .line 634
    :cond_5b
    return-void
.end method

.method public static manageDecodeParts(Landroid/content/Context;Ljava/lang/String;IIII)Ljava/util/HashMap;
    .registers 25
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "encodedJson"    # Ljava/lang/String;
    .param p2, "partNumber"    # I
    .param p3, "totalParts"    # I
    .param p4, "subpartNumber"    # I
    .param p5, "totalSubparts"    # I
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0
        }
        names = {
            "context",
            "encodedJson",
            "partNumber",
            "totalParts",
            "subpartNumber",
            "totalSubparts"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/content/Context;",
            "Ljava/lang/String;",
            "IIII)",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .line 301
    move/from16 v1, p2

    move/from16 v2, p3

    move/from16 v3, p4

    const-string v0, "_total_subparts"

    const-string v4, "_subpart_"

    const-string v5, "log_part_"

    :try_start_c
    sget-object v6, L{}/ApkStringDecodeCommon;->PREF_LOG_DECODE:Ljava/lang/String;

    const/4 v7, 0x0

    move-object/from16 v8, p0

    invoke-virtual {v8, v6, v7}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v6

    .line 302
    .local v6, "prefs":Landroid/content/SharedPreferences;
    invoke-interface {v6}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v7

    .line 305
    .local v7, "editor":Landroid/content/SharedPreferences$Editor;
    new-instance v9, Ljava/lang/StringBuilder;

    invoke-direct {v9}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v9, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v9, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v9, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v9, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v9
    :try_end_2e
    .catch Ljava/lang/Exception; {:try_start_c .. :try_end_2e} :catch_177

    .line 306
    .local v9, "subpartKey":Ljava/lang/String;
    move-object/from16 v10, p1

    :try_start_30
    invoke-interface {v7, v9, v10}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;

    .line 309
    new-instance v11, Ljava/lang/StringBuilder;

    invoke-direct {v11}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v11, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v11, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v11, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v11}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v11

    .line 310
    .local v11, "totalSubpartsKey":Ljava/lang/String;
    invoke-interface {v6, v11}, Landroid/content/SharedPreferences;->contains(Ljava/lang/String;)Z

    move-result v12
    :try_end_49
    .catch Ljava/lang/Exception; {:try_start_30 .. :try_end_49} :catch_175

    if-nez v12, :cond_51

    .line 311
    move/from16 v12, p5

    :try_start_4d
    invoke-interface {v7, v11, v12}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;

    goto :goto_53

    .line 310
    :cond_51
    move/from16 v12, p5

    .line 314
    :goto_53
    invoke-interface {v7}, Landroid/content/SharedPreferences$Editor;->apply()V

    .line 316
    sget-object v13, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v14, Ljava/lang/StringBuilder;

    invoke-direct {v14}, Ljava/lang/StringBuilder;-><init>()V

    const-string v15, "Received part: "

    invoke-virtual {v14, v15}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v14, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v15, ", subpart: "

    invoke-virtual {v14, v15}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v14, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v14}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v14

    invoke-static {v13, v14}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 319
    const/4 v13, 0x1

    .line 321
    .local v13, "allPartsReceived":Z
    const/4 v14, 0x1

    .local v14, "partIndex":I
    :goto_76
    if-gt v14, v2, :cond_eb

    .line 322
    new-instance v15, Ljava/lang/StringBuilder;

    invoke-direct {v15}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v15, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v15, v14}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v15, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v15}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v15

    const/4 v1, 0x1

    invoke-interface {v6, v15, v1}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result v15

    move v1, v15

    .line 324
    .local v1, "totalSubpartsForPart":I
    const/4 v15, 0x1

    .local v15, "subpartIndex":I
    :goto_91
    if-gt v15, v1, :cond_dd

    .line 325
    move/from16 v17, v1

    .end local v1    # "totalSubpartsForPart":I
    .local v17, "totalSubpartsForPart":I
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v14}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v15}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    .line 326
    .local v1, "subpartKeyCheck":Ljava/lang/String;
    invoke-interface {v6, v1}, Landroid/content/SharedPreferences;->contains(Ljava/lang/String;)Z

    move-result v18

    if-nez v18, :cond_d2

    .line 327
    const/4 v13, 0x0

    .line 328
    move-object/from16 v18, v1

    .end local v1    # "subpartKeyCheck":Ljava/lang/String;
    .local v18, "subpartKeyCheck":Ljava/lang/String;
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v8, "Missing subpart: "

    invoke-virtual {v3, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v15}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v8, " for part: "

    invoke-virtual {v3, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v14}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v1, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 329
    goto :goto_df

    .line 326
    .end local v18    # "subpartKeyCheck":Ljava/lang/String;
    .restart local v1    # "subpartKeyCheck":Ljava/lang/String;
    :cond_d2
    move-object/from16 v18, v1

    .line 324
    .end local v1    # "subpartKeyCheck":Ljava/lang/String;
    add-int/lit8 v15, v15, 0x1

    move-object/from16 v8, p0

    move/from16 v3, p4

    move/from16 v1, v17

    goto :goto_91

    .end local v17    # "totalSubpartsForPart":I
    .local v1, "totalSubpartsForPart":I
    :cond_dd
    move/from16 v17, v1

    .line 333
    .end local v1    # "totalSubpartsForPart":I
    .end local v15    # "subpartIndex":I
    .restart local v17    # "totalSubpartsForPart":I
    :goto_df
    if-nez v13, :cond_e2

    .line 334
    goto :goto_eb

    .line 321
    .end local v17    # "totalSubpartsForPart":I
    :cond_e2
    add-int/lit8 v14, v14, 0x1

    move-object/from16 v8, p0

    move/from16 v1, p2

    move/from16 v3, p4

    goto :goto_76

    .line 338
    .end local v14    # "partIndex":I
    :cond_eb
    :goto_eb
    if-eqz v13, :cond_172

    .line 339
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v3, "All parts and subparts received - Decoding and merging final map"

    invoke-static {v1, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 342
    new-instance v1, Ljava/util/HashMap;

    invoke-direct {v1}, Ljava/util/HashMap;-><init>()V

    .line 344
    .local v1, "finalDecodedMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    const/4 v3, 0x1

    .local v3, "partIndex":I
    :goto_fa
    if-gt v3, v2, :cond_16b

    .line 345
    new-instance v8, Ljava/lang/StringBuilder;

    invoke-direct {v8}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v8, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v8, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v8, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v8}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    const/4 v14, 0x1

    invoke-interface {v6, v8, v14}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result v8

    .line 346
    .local v8, "totalSubpartsForPart":I
    new-instance v15, Ljava/lang/StringBuilder;

    invoke-direct {v15}, Ljava/lang/StringBuilder;-><init>()V

    .line 348
    .local v15, "combinedSubparts":Ljava/lang/StringBuilder;
    const/16 v16, 0x1

    move/from16 v14, v16

    .local v14, "subpartIndex":I
    :goto_11c
    if-gt v14, v8, :cond_151

    .line 349
    move-object/from16 v16, v0

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v14}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 350
    .local v0, "subpartKeyToProcess":Ljava/lang/String;
    const-string v2, ""

    invoke-interface {v6, v0, v2}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 352
    .local v2, "encodedSubpart":Ljava/lang/String;
    if-eqz v2, :cond_14a

    invoke-virtual {v2}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v18

    invoke-virtual/range {v18 .. v18}, Ljava/lang/String;->isEmpty()Z

    move-result v18

    if-nez v18, :cond_14a

    .line 353
    invoke-virtual {v15, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 348
    .end local v0    # "subpartKeyToProcess":Ljava/lang/String;
    .end local v2    # "encodedSubpart":Ljava/lang/String;
    :cond_14a
    add-int/lit8 v14, v14, 0x1

    move/from16 v2, p3

    move-object/from16 v0, v16

    goto :goto_11c

    :cond_151
    move-object/from16 v16, v0

    .line 357
    .end local v14    # "subpartIndex":I
    invoke-virtual {v15}, Ljava/lang/StringBuilder;->length()I

    move-result v0

    if-lez v0, :cond_164

    .line 359
    invoke-virtual {v15}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, L{}/ApkStringDecodeCommon;->decodeBase64ToHashMap(Ljava/lang/String;)Ljava/util/HashMap;

    move-result-object v0

    .line 360
    .local v0, "decodedPartMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    invoke-virtual {v1, v0}, Ljava/util/HashMap;->putAll(Ljava/util/Map;)V

    .line 344
    .end local v0    # "decodedPartMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v8    # "totalSubpartsForPart":I
    .end local v15    # "combinedSubparts":Ljava/lang/StringBuilder;
    :cond_164
    add-int/lit8 v3, v3, 0x1

    move/from16 v2, p3

    move-object/from16 v0, v16

    goto :goto_fa

    .line 365
    .end local v3    # "partIndex":I
    :cond_16b
    invoke-interface {v7}, Landroid/content/SharedPreferences$Editor;->clear()Landroid/content/SharedPreferences$Editor;

    .line 366
    invoke-interface {v7}, Landroid/content/SharedPreferences$Editor;->apply()V
    :try_end_171
    .catch Ljava/lang/Exception; {:try_start_4d .. :try_end_171} :catch_173

    .line 368
    return-object v1

    .line 374
    .end local v1    # "finalDecodedMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v6    # "prefs":Landroid/content/SharedPreferences;
    .end local v7    # "editor":Landroid/content/SharedPreferences$Editor;
    .end local v9    # "subpartKey":Ljava/lang/String;
    .end local v11    # "totalSubpartsKey":Ljava/lang/String;
    .end local v13    # "allPartsReceived":Z
    :cond_172
    goto :goto_17f

    .line 372
    :catch_173
    move-exception v0

    goto :goto_17c

    :catch_175
    move-exception v0

    goto :goto_17a

    :catch_177
    move-exception v0

    move-object/from16 v10, p1

    :goto_17a
    move/from16 v12, p5

    .line 373
    .local v0, "e":Ljava/lang/Exception;
    :goto_17c
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 377
    .end local v0    # "e":Ljava/lang/Exception;
    :goto_17f
    const/4 v0, 0x0

    return-object v0
.end method

.method private static parseByteArray(Ljava/lang/String;)[B
    .registers 5
    .param p0, "byteArrayString"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "byteArrayString"
        }
    .end annotation

    .line 402
    const-string v0, "t"

    const-string v1, ""

    invoke-virtual {p0, v0, v1}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const-string v1, ","

    invoke-virtual {v0, v1}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v0

    .line 403
    .local v0, "byteStrings":[Ljava/lang/String;
    array-length v1, v0

    new-array v1, v1, [B

    .line 405
    .local v1, "byteArray":[B
    const/4 v2, 0x0

    .local v2, "i":I
    :goto_12
    array-length v3, v0

    if-ge v2, v3, :cond_25

    .line 407
    aget-object v3, v0, v2

    invoke-static {v3}, Ljava/lang/Integer;->decode(Ljava/lang/String;)Ljava/lang/Integer;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/Integer;->intValue()I

    move-result v3

    int-to-byte v3, v3

    aput-byte v3, v1, v2

    .line 405
    add-int/lit8 v2, v2, 0x1

    goto :goto_12

    .line 410
    .end local v2    # "i":I
    :cond_25
    return-object v1
.end method

.method public static pingCollected(Landroid/content/Context;)V
    .registers 3
    .param p0, "context"    # Landroid/content/Context;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "context"
        }
    .end annotation

    .line 90
    sget-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "Ping Received."

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 91
    invoke-static {p0}, L{}/ApkStringDecodeCommon;->clearSharePreferencesLogs(Landroid/content/Context;)V

    .line 92
    invoke-static {p0}, L{}/ApkStringDecodeCommon;->createDecodeFileIfNotExists(Landroid/content/Context;)V

    .line 93
    invoke-static {p0}, L{}/ApkStringDecodeCommon;->setTaskFlagAsNotDone(Landroid/content/Context;)V

    .line 94
    return-void
.end method

.method public static printLogError(Ljava/lang/Exception;)V
    .registers 7
    .param p0, "e"    # Ljava/lang/Exception;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "e"
        }
    .end annotation

    .line 660
    new-instance v0, Ljava/io/StringWriter;

    invoke-direct {v0}, Ljava/io/StringWriter;-><init>()V

    .line 661
    .local v0, "sw":Ljava/io/StringWriter;
    new-instance v1, Ljava/io/PrintWriter;

    invoke-direct {v1, v0}, Ljava/io/PrintWriter;-><init>(Ljava/io/Writer;)V

    .line 662
    .local v1, "pw":Ljava/io/PrintWriter;
    invoke-virtual {p0, v1}, Ljava/lang/Exception;->printStackTrace(Ljava/io/PrintWriter;)V

    .line 663
    invoke-virtual {v0}, Ljava/io/StringWriter;->toString()Ljava/lang/String;

    move-result-object v2

    .line 664
    .local v2, "stackTrace":Ljava/lang/String;
    sget-object v3, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    const-string v5, "Exception occurred with stack trace: "

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {v3, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 665
    return-void
.end method

.method private static processHashMap(Lorg/json/JSONObject;)Ljava/util/HashMap;
    .registers 7
    .param p0, "jsonObject"    # Lorg/json/JSONObject;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "jsonObject"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lorg/json/JSONObject;",
            ")",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lorg/json/JSONException;
        }
    .end annotation

    .line 561
    new-instance v0, Ljava/util/HashMap;

    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    .line 564
    .local v0, "hashMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    invoke-virtual {p0}, Lorg/json/JSONObject;->keys()Ljava/util/Iterator;

    move-result-object v1

    .line 565
    .local v1, "keys":Ljava/util/Iterator;, "Ljava/util/Iterator<Ljava/lang/String;>;"
    :goto_9
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    move-result v2

    if-eqz v2, :cond_2e

    .line 566
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    .line 567
    .local v2, "key":Ljava/lang/String;
    invoke-virtual {p0, v2}, Lorg/json/JSONObject;->get(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v3

    .line 571
    .local v3, "jsonElement":Ljava/lang/Object;
    instance-of v4, v3, Lorg/json/JSONArray;

    if-eqz v4, :cond_26

    .line 572
    move-object v4, v3

    check-cast v4, Lorg/json/JSONArray;

    .line 574
    .local v4, "jsonArray":Lorg/json/JSONArray;
    const/4 v5, 0x0

    invoke-virtual {v4, v5}, Lorg/json/JSONArray;->getString(I)Ljava/lang/String;

    move-result-object v4

    .line 575
    .local v4, "value":Ljava/lang/String;
    goto :goto_2a

    .line 577
    .end local v4    # "value":Ljava/lang/String;
    :cond_26
    invoke-virtual {p0, v2}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    .line 579
    .restart local v4    # "value":Ljava/lang/String;
    :goto_2a
    invoke-virtual {v0, v2, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 580
    .end local v2    # "key":Ljava/lang/String;
    .end local v3    # "jsonElement":Ljava/lang/Object;
    .end local v4    # "value":Ljava/lang/String;
    goto :goto_9

    .line 582
    :cond_2e
    return-object v0
.end method

.method private static sanitizeStringValue(Ljava/lang/String;)Ljava/lang/String;
    .registers 8
    .param p0, "input"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "input"
        }
    .end annotation

    .line 586
    invoke-static {p0}, L{}/ApkStringDecodeCommon;->decodeUnicodeEscapes(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 587
    .local v0, "decoded":Ljava/lang/String;
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    .line 588
    .local v1, "sanitized":Ljava/lang/StringBuilder;
    invoke-virtual {v0}, Ljava/lang/String;->toCharArray()[C

    move-result-object v2

    array-length v3, v2

    const/4 v4, 0x0

    :goto_f
    if-ge v4, v3, :cond_31

    aget-char v5, v2, v4

    .line 589
    .local v5, "c":C
    invoke-static {v5}, Ljava/lang/Character;->isISOControl(C)Z

    move-result v6

    if-eqz v6, :cond_2b

    const/16 v6, 0xa

    if-eq v5, v6, :cond_2b

    const/16 v6, 0xd

    if-eq v5, v6, :cond_2b

    const/16 v6, 0x9

    if-eq v5, v6, :cond_2b

    .line 591
    const-string v6, " "

    invoke-virtual {v1, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_2e

    .line 593
    :cond_2b
    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 588
    .end local v5    # "c":C
    :goto_2e
    add-int/lit8 v4, v4, 0x1

    goto :goto_f

    .line 596
    :cond_31
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    return-object v2
.end method

.method public static saveDecodedResultToFile(Landroid/content/Context;Ljava/util/HashMap;)V
    .registers 11
    .param p0, "context"    # Landroid/content/Context;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0
        }
        names = {
            "context",
            "decodedResult"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/content/Context;",
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;)V"
        }
    .end annotation

    .line 251
    .local p1, "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    if-eqz p1, :cond_f4

    invoke-virtual {p1}, Ljava/util/HashMap;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_a

    goto/16 :goto_f4

    .line 256
    :cond_a
    new-instance v0, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v1

    sget-object v2, L{}/ApkStringDecodeCommon;->FILE_DECODED_STRINGS:Ljava/lang/String;

    invoke-direct {v0, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 257
    .local v0, "fileToDelete":Ljava/io/File;
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v1

    if-eqz v1, :cond_35

    .line 258
    invoke-virtual {v0}, Ljava/io/File;->delete()Z

    move-result v1

    .line 259
    .local v1, "deleted":Z
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "Deleted old results file: "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Z)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 262
    .end local v1    # "deleted":Z
    :cond_35
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "saveDecodedResultToFile() called with map size: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/util/HashMap;->size()I

    move-result v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 266
    :try_start_4f
    new-instance v1, Ljava/util/HashMap;

    invoke-direct {v1}, Ljava/util/HashMap;-><init>()V

    .line 267
    .local v1, "cleanMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    invoke-virtual {p1}, Ljava/util/HashMap;->entrySet()Ljava/util/Set;

    move-result-object v2

    invoke-interface {v2}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    move-result-object v2

    :goto_5c
    invoke-interface {v2}, Ljava/util/Iterator;->hasNext()Z

    move-result v3

    if-eqz v3, :cond_82

    invoke-interface {v2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Ljava/util/Map$Entry;

    .line 268
    .local v3, "entry":Ljava/util/Map$Entry;, "Ljava/util/Map$Entry<**>;"
    invoke-interface {v3}, Ljava/util/Map$Entry;->getKey()Ljava/lang/Object;

    move-result-object v4

    .line 269
    .local v4, "key":Ljava/lang/Object;
    invoke-interface {v3}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    move-result-object v5

    .line 270
    .local v5, "value":Ljava/lang/Object;
    instance-of v6, v4, Ljava/lang/String;

    if-eqz v6, :cond_81

    instance-of v6, v5, Ljava/lang/String;

    if-eqz v6, :cond_81

    .line 271
    move-object v6, v4

    check-cast v6, Ljava/lang/String;

    move-object v7, v5

    check-cast v7, Ljava/lang/String;

    invoke-virtual {v1, v6, v7}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 273
    .end local v3    # "entry":Ljava/util/Map$Entry;, "Ljava/util/Map$Entry<**>;"
    .end local v4    # "key":Ljava/lang/Object;
    .end local v5    # "value":Ljava/lang/Object;
    :cond_81
    goto :goto_5c

    .line 276
    :cond_82
    new-instance v2, Lorg/json/JSONObject;

    invoke-direct {v2, v1}, Lorg/json/JSONObject;-><init>(Ljava/util/Map;)V

    .line 277
    .local v2, "jsonObject":Lorg/json/JSONObject;
    const/4 v3, 0x2

    invoke-virtual {v2, v3}, Lorg/json/JSONObject;->toString(I)Ljava/lang/String;

    move-result-object v3

    .line 280
    .local v3, "jsonString":Ljava/lang/String;
    new-instance v4, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v5

    sget-object v6, L{}/ApkStringDecodeCommon;->FILE_DECODED_STRINGS:Ljava/lang/String;

    invoke-direct {v4, v5, v6}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 281
    .local v4, "file":Ljava/io/File;
    new-instance v5, Ljava/io/BufferedWriter;

    new-instance v6, Ljava/io/OutputStreamWriter;

    new-instance v7, Ljava/io/FileOutputStream;

    const/4 v8, 0x0

    invoke-direct {v7, v4, v8}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;Z)V

    sget-object v8, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-direct {v6, v7, v8}, Ljava/io/OutputStreamWriter;-><init>(Ljava/io/OutputStream;Ljava/nio/charset/Charset;)V

    invoke-direct {v5, v6}, Ljava/io/BufferedWriter;-><init>(Ljava/io/Writer;)V
    :try_end_a9
    .catch Ljava/lang/Exception; {:try_start_4f .. :try_end_a9} :catch_d5

    .line 283
    .local v5, "writer":Ljava/io/BufferedWriter;
    :try_start_a9
    invoke-virtual {v5, v3}, Ljava/io/BufferedWriter;->write(Ljava/lang/String;)V

    .line 284
    invoke-virtual {v5}, Ljava/io/BufferedWriter;->flush()V
    :try_end_af
    .catchall {:try_start_a9 .. :try_end_af} :catchall_ce

    .line 285
    :try_start_af
    invoke-virtual {v5}, Ljava/io/BufferedWriter;->close()V

    .line 287
    .end local v5    # "writer":Ljava/io/BufferedWriter;
    sget-object v5, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    const-string v7, "Decoded results saved to file: "

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v6

    invoke-static {v5, v6}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I
    :try_end_cc
    .catch Ljava/lang/Exception; {:try_start_af .. :try_end_cc} :catch_d5

    .line 292
    nop

    .end local v1    # "cleanMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v2    # "jsonObject":Lorg/json/JSONObject;
    .end local v3    # "jsonString":Ljava/lang/String;
    .end local v4    # "file":Ljava/io/File;
    goto :goto_f3

    .line 281
    .restart local v1    # "cleanMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .restart local v2    # "jsonObject":Lorg/json/JSONObject;
    .restart local v3    # "jsonString":Ljava/lang/String;
    .restart local v4    # "file":Ljava/io/File;
    .restart local v5    # "writer":Ljava/io/BufferedWriter;
    :catchall_ce
    move-exception v6

    :try_start_cf
    invoke-virtual {v5}, Ljava/io/BufferedWriter;->close()V
    :try_end_d2
    .catchall {:try_start_cf .. :try_end_d2} :catchall_d3

    goto :goto_d4

    :catchall_d3
    move-exception v7

    .end local v0    # "fileToDelete":Ljava/io/File;
    .end local p0    # "context":Landroid/content/Context;
    .end local p1    # "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    :goto_d4
    :try_start_d4
    throw v6
    :try_end_d5
    .catch Ljava/lang/Exception; {:try_start_d4 .. :try_end_d5} :catch_d5

    .line 289
    .end local v1    # "cleanMap":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    .end local v2    # "jsonObject":Lorg/json/JSONObject;
    .end local v3    # "jsonString":Ljava/lang/String;
    .end local v4    # "file":Ljava/io/File;
    .end local v5    # "writer":Ljava/io/BufferedWriter;
    .restart local v0    # "fileToDelete":Ljava/io/File;
    .restart local p0    # "context":Landroid/content/Context;
    .restart local p1    # "decodedResult":Ljava/util/HashMap;, "Ljava/util/HashMap<Ljava/lang/String;Ljava/lang/String;>;"
    :catch_d5
    move-exception v1

    .line 290
    .local v1, "e":Ljava/lang/Exception;
    invoke-virtual {v1}, Ljava/lang/Exception;->printStackTrace()V

    .line 291
    sget-object v2, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "Failed to save decoded results: "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 293
    .end local v1    # "e":Ljava/lang/Exception;
    :goto_f3
    return-void

    .line 252
    .end local v0    # "fileToDelete":Ljava/io/File;
    :cond_f4
    :goto_f4
    sget-object v0, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    const-string v1, "Decoded result is empty. File will not be created."

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 253
    return-void
.end method

.method private static setTaskFlag(Landroid/content/Context;Ljava/lang/String;)V
    .registers 6
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "state"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0
        }
        names = {
            "context",
            "state"
        }
    .end annotation

    .line 138
    :try_start_0
    new-instance v0, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v1

    sget-object v2, L{}/ApkStringDecodeCommon;->BEHAVIOR_STATUS_TASK_FLAG_FILE:Ljava/lang/String;

    invoke-direct {v0, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 139
    .local v0, "file":Ljava/io/File;
    new-instance v1, Ljava/io/FileOutputStream;

    invoke-direct {v1, v0}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    .line 140
    .local v1, "fos":Ljava/io/FileOutputStream;
    new-instance v2, Ljava/io/OutputStreamWriter;

    const-string v3, "UTF-8"

    invoke-direct {v2, v1, v3}, Ljava/io/OutputStreamWriter;-><init>(Ljava/io/OutputStream;Ljava/lang/String;)V

    .line 141
    .local v2, "writer":Ljava/io/OutputStreamWriter;
    invoke-virtual {v2, p1}, Ljava/io/OutputStreamWriter;->write(Ljava/lang/String;)V

    .line 142
    invoke-virtual {v2}, Ljava/io/OutputStreamWriter;->close()V

    .line 143
    invoke-virtual {v1}, Ljava/io/FileOutputStream;->close()V
    :try_end_20
    .catch Ljava/io/FileNotFoundException; {:try_start_0 .. :try_end_20} :catch_29
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_20} :catch_21

    .end local v0    # "file":Ljava/io/File;
    .end local v1    # "fos":Ljava/io/FileOutputStream;
    .end local v2    # "writer":Ljava/io/OutputStreamWriter;
    goto :goto_30

    .line 147
    :catch_21
    move-exception v0

    .line 148
    .local v0, "e":Ljava/io/IOException;
    invoke-virtual {v0}, Ljava/io/IOException;->printStackTrace()V

    .line 149
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    goto :goto_31

    .line 144
    .end local v0    # "e":Ljava/io/IOException;
    :catch_29
    move-exception v0

    .line 145
    .local v0, "e":Ljava/io/FileNotFoundException;
    invoke-virtual {v0}, Ljava/io/FileNotFoundException;->printStackTrace()V

    .line 146
    invoke-static {v0}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 150
    .end local v0    # "e":Ljava/io/FileNotFoundException;
    :goto_30
    nop

    .line 151
    :goto_31
    return-void
.end method

.method private static setTaskFlagAsDone(Landroid/content/Context;)V
    .registers 2
    .param p0, "context"    # Landroid/content/Context;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "context"
        }
    .end annotation

    .line 129
    sget-object v0, L{}/ApkStringDecodeCommon;->BEHAVIOR_STATUS_TRUE:Ljava/lang/String;

    invoke-static {p0, v0}, L{}/ApkStringDecodeCommon;->setTaskFlag(Landroid/content/Context;Ljava/lang/String;)V

    .line 130
    return-void
.end method

.method private static setTaskFlagAsNotDone(Landroid/content/Context;)V
    .registers 2
    .param p0, "context"    # Landroid/content/Context;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "context"
        }
    .end annotation

    .line 133
    sget-object v0, L{}/ApkStringDecodeCommon;->BEHAVIOR_STATUS_FALSE:Ljava/lang/String;

    invoke-static {p0, v0}, L{}/ApkStringDecodeCommon;->setTaskFlag(Landroid/content/Context;Ljava/lang/String;)V

    .line 134
    return-void
.end method

.method public static singleDecode(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .registers 13
    .param p0, "context"    # Landroid/content/Context;
    .param p1, "className"    # Ljava/lang/String;
    .param p2, "methodName"    # Ljava/lang/String;
    .param p3, "javaSignature"    # Ljava/lang/String;
    .param p4, "argumentsString"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0,
            0x0,
            0x0,
            0x0,
            0x0
        }
        names = {
            "context",
            "className",
            "methodName",
            "javaSignature",
            "argumentsString"
        }
    .end annotation

    .line 156
    sget-object v0, L{}/ApkStringDecodeCommon;->DECODE_CLASS_DECODING_ERROR:Ljava/lang/String;

    .line 158
    .local v0, "decodedValue":Ljava/lang/String;
    const/4 v7, 0x0

    move-object v1, p0

    move-object v2, p1

    move-object v3, p2

    move-object v4, p3

    move-object v5, p4

    move-object v6, p4

    :try_start_9
    invoke-static/range {v1 .. v7}, L{}/ApkStringDecodeCommon;->invokeMethodWithSignature(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    move-result-object v1

    move-object v0, v1

    .line 160
    sget-object v1, L{}/ApkStringDecodeCommon;->LOG_TAG_STANDARD:Ljava/lang/String;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "Original: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, p4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v3, ", Decoded: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I
    :try_end_2c
    .catch Ljava/lang/Exception; {:try_start_9 .. :try_end_2c} :catch_2d

    .line 165
    goto :goto_34

    .line 162
    :catch_2d
    move-exception v1

    .line 163
    .local v1, "e":Ljava/lang/Exception;
    invoke-virtual {v1}, Ljava/lang/Exception;->printStackTrace()V

    .line 164
    invoke-static {v1}, L{}/ApkStringDecodeCommon;->printLogError(Ljava/lang/Exception;)V

    .line 166
    .end local v1    # "e":Ljava/lang/Exception;
    :goto_34
    return-void
.end method

.method public static unescapeJavaString(Ljava/lang/String;)Ljava/lang/String;
    .registers 6
    .param p0, "escapedStr"    # Ljava/lang/String;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x0
        }
        names = {
            "escapedStr"
        }
    .end annotation

    .line 637
    if-nez p0, :cond_4

    .line 638
    const/4 v0, 0x0

    return-object v0

    .line 640
    :cond_4
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(I)V

    .line 642
    .local v0, "sb":Ljava/lang/StringBuilder;
    const/4 v1, 0x0

    .local v1, "i":I
    :goto_e
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v2

    if-ge v1, v2, :cond_47

    .line 643
    invoke-virtual {p0, v1}, Ljava/lang/String;->charAt(I)C

    move-result v2

    .line 644
    .local v2, "c":C
    const/16 v3, 0x5c

    if-ne v2, v3, :cond_41

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    add-int/lit8 v3, v3, -0x1

    if-ge v1, v3, :cond_41

    .line 645
    add-int/lit8 v3, v1, 0x1

    invoke-virtual {p0, v3}, Ljava/lang/String;->charAt(I)C

    move-result v3

    .line 646
    .local v3, "nextChar":C
    sparse-switch v3, :sswitch_data_4c

    .line 650
    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    goto :goto_40

    .line 648
    :sswitch_31
    const/16 v4, 0x9

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    add-int/lit8 v1, v1, 0x1

    goto :goto_40

    .line 647
    :sswitch_39
    const/16 v4, 0xa

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    add-int/lit8 v1, v1, 0x1

    .line 652
    .end local v3    # "nextChar":C
    :goto_40
    goto :goto_44

    .line 653
    :cond_41
    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 642
    .end local v2    # "c":C
    :goto_44
    add-int/lit8 v1, v1, 0x1

    goto :goto_e

    .line 656
    .end local v1    # "i":I
    :cond_47
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    return-object v1

    :sswitch_data_4c
    .sparse-switch
        0x6e -> :sswitch_39
        0x74 -> :sswitch_31
    .end sparse-switch
.end method
"""