# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils import timezone
from accounts.models import User
from dailyreport.models import Daily
from dailyreport.forms import SearchForm, DateForm, TaskSearchForm, DailySearchForm
from dailyreport.services.service_comment import \
    get_comments_from_daily, get_or_create_comment, edit_comment, delete_comment_record
from dailyreport.services.service_daily import \
    get_all_daily_list, get_user_daily_list, get_or_create_daily, edit_daily, delete_daily_record
from dailyreport.services.service_task import \
    create_task_form_in_queryset, get_task_from_implement_date, get_task_from_create_date, \
    get_next_task, get_all_task, edit_task, get_narrowing_task
from dailyreport.services.service_utility import init_dictionary, create_pagination


u"""views.py
    各関数は、辞書型で引数をまとめ、renderにhtmlファイルの指定とともに渡します
    本ファイル中で、直接モデルにアクセスする処理は書かないようにしています
        services.pyで行います

    各関数ではservices.init_dictionary()を呼んでいます
    init_dictionary()は、検索フォームなど共通の情報を初期情報として登録するためのものです
    daily_list()において軽く触れますが、以降の関数では触れませんのでご了承ください

    NAME最後の()内は対応するCRUDの属性です
        ex) 日報詳細(R)
            RはReadの頭文字であり、日報詳細はCRUDのRに対応する関数である
        なお、すべてのモデルに対して、すべてのCRUDを実装しているわけではありません
"""


@login_required
def daily_list_view(request):
    u"""日報一覧
        日報の一覧を取得し、レンダリングを指示します

        dictionary:
            init:キーワード検索フォーム
            init:日付絞込みフォーム
            公開済みの全日報のクエリセット
            当日分のタスク一覧(フォーム形式)
            明日以降分のタスク一覧(フォーム形式)
    :param request: 関数が呼ばれたときにhtmlから送られてきた情報。ここでは使用しない。
    :return:レンダリング対象のhtmlファイル'dailyreport/daily_list.html'、およびhtmlファイル中で利用するフォーム・クエリリスト
    """
    dictionary = init_dictionary(request=request)
    dictionary.update(pages=create_pagination(request, get_all_daily_list(request=request, release=True)))
    dictionary.update(dailys=dictionary['pages'].object_list)
    dictionary.update(is_paginated=True)
    dictionary.update(date_form=DateForm(request.GET))
    dictionary.update(task_form=create_task_form_in_queryset(
        get_task_from_implement_date(request.user, timezone.now().date())
    ))
    dictionary.update(task_form_next=create_task_form_in_queryset(
        get_next_task(request.user, timezone.now().date())
    ))

    return render_to_response('dailyreport/daily_list.html', dictionary, context_instance=RequestContext(request))


@login_required
def daily_detail_view(request, daily_id):
    u"""日報詳細(R)
        日報の詳細を取得し、レンダリングを指示します
        表示対象は以下の通り
            ある日報のレコード
            日報の作成日に実施されたタスク
            日報の作成日に作成されたタスク
        dictionary:
            日報
            日報の作成日に実施されたタスク(implement_date)
            日報の作成日に作成されたタスク(create_date)
            日報に紐付けられたコメント一覧
            コメント入力フォーム
            当日分のタスク一覧(フォーム形式)
            明日以降分のタスク一覧(フォーム形式)
    :param request: ユーザー情報の取得
    :param daily_id: 表示対象の日報取得
    :return: レンダリング対象のhtmlファイル'dailyreport/daily_detail.html'、およびhtmlファイル中で利用するフォーム・クエリリスト
    """
    dictionary = init_dictionary(request=request, daily_id=daily_id)
    dictionary.update(daily=get_or_create_daily(daily_id=daily_id))
    dictionary.update(comments=get_comments_from_daily(dictionary['daily']))
    dictionary.update(task_form=create_task_form_in_queryset(
        get_task_from_implement_date(request.user, timezone.now().date())
    ))
    dictionary.update(task_form_next=create_task_form_in_queryset(
        get_next_task(request.user, timezone.now().date())
    ))
    dictionary.update(implement_task=get_task_from_implement_date(
        user=dictionary['daily'].user, date=dictionary['daily'].create_date))
    dictionary.update(create_task=get_task_from_create_date(
        user=dictionary['daily'].user, date=dictionary['daily'].create_date))
    flag, dictionary['comment_form'] = edit_comment(
        request=request, daily=dictionary['daily'],  comment=get_or_create_comment(request.user))

    return render_to_response('dailyreport/daily_detail.html', dictionary, context_instance=RequestContext(request))


def daily_edit_view(request, daily_id=None):
    u"""日報編集(U)
        日報を編集し、編集後の日報詳細を表示する
        表示対象は以下の通り
            日報
            日報の作成日または当日(新規作成時)に実施されたタスク
            日報の作成日または当日(新規作成時)に作成されたタスク
        なお、日報編集ページではタスクの編集は行わない
            トップページなどの画面中に表示されているタスク編集フォームを利用して逐次更新が行われているものとする
        dictionary:
            日報
            日報編集用フォーム
                idが指定されている場合は日報を取得後、フォームとする
                idが未指定の場合には、新規日報のインスタンスを作成し、フォームとする
            日報の作成日または当日(新規作成時)に実施されたタスク(implement_date)
            日報の作成日または当日(新規作成時)に作成されたタスク(create_date)
    :param request: ユーザー情報の取得
    :param daily_id: 編集対象の日報id(未指定の場合新規作成と判断)
    :return: レンダリング対象のhtmlファイル'dailyreport/daily_edit.html'、およびhtmlファイル中で利用するフォーム・クエリリスト
    """
    dictionary = init_dictionary(request=request, daily_id=daily_id)
    dictionary.update(daily=get_or_create_daily(user=request.user, daily_id=daily_id))
    if request.user != dictionary['daily'].user:
        return redirect('login')
    flag, dictionary['report_form'] = edit_daily(request=request, daily=dictionary['daily'])
    dictionary.update(task_form=create_task_form_in_queryset(
        get_task_from_implement_date(request.user, timezone.now().date())
    ))
    dictionary.update(task_form_next=create_task_form_in_queryset(
        get_next_task(request.user, timezone.now().date())
    ))

    if daily_id:
        dictionary.update(implement_task=get_task_from_implement_date(
            dictionary['daily'].user, dictionary['daily'].create_date))
        dictionary.update(create_task=get_task_from_create_date(
            dictionary['daily'].user, dictionary['daily'].create_date))
    else:
        dictionary.update(implement_task=get_task_from_implement_date(request.user, timezone.now().date()))
        dictionary.update(create_task=get_task_from_create_date(request.user, timezone.now().date()))

    if request.method == 'POST' and flag:
        return redirect('dailyreport:view_daily_detail', daily_id=dictionary['report_form'].id)
    elif flag is False:
        return render_to_response('dailyreport/daily_edit.html', dictionary, context_instance=RequestContext(request))

    if 'gototask' in request.POST:
        return redirect('dailyreport:edit_task')

    return render_to_response('dailyreport/daily_edit.html', dictionary, context_instance=RequestContext(request))


def edit_task_in_task_page(request):
    u"""タスク一覧(CRU)
        タスク一覧をフォームとして表示します
        表示対象のタスクはユーザーそれぞれのタスクのみです
        R属性は仮です
            タスク単独を詳しく編集するフォームを実装する可能性があります
        dictionary:
        タスクフォーム
    :param request:ユーザー情報の取得
    :return:レンダリング対象のhtmlファイル'dailyreport/task_list.html'、およびhtmlファイル中で利用するフォーム
    """
    dictionary = init_dictionary(request=request)
    edit_task(request)
    dictionary.update(task_search_form=TaskSearchForm(request.GET))

    dictionary.update(tasks=create_pagination(request, get_narrowing_task(request=request)))
    dictionary.update(task_form=create_task_form_in_queryset(dictionary['tasks'].object_list))
    return render_to_response('dailyreport/task_list.html', dictionary, context_instance=RequestContext(request))


def edit_task_in_daily_page(request):
    u"""タスク一覧(CRU)
        日報表示部分を持つページにおいてタスクを更新するためのメソッドです
        通常のものと比べ、返るページが異なります
        表示対象のタスクはユーザーそれぞれのタスクのみです
        R属性は仮です
            タスク単独を詳しく編集するフォームを実装する可能性があります
        lists:
        タスクフォーム
    :param request:ユーザー情報の取得
    :return:レンダリング対象のhtmlファイル'dailyreport/task_list.html'、およびhtmlファイル中で利用するフォーム
    """
    edit_task(request)

    return redirect('dailyreport:view_daily_list')


def narrowing_task_by_date(request):
    u"""タスク日付絞込み
        タスクの一覧を日付で絞り込みます
        表示対象のタスクはtask_editと同じくユーザーそれぞれのタスクのみです
        DateFormフォームより送られてきた日付情報をもとに、タスクフォームセットに表示する情報を絞り込みます
            絞り込む対象は実施日(implement_date)です
            タスクの作成日(create_date)ではありません
    :param request: dateform(日付をカレンダーによって指定するフォーム)からのリクエスト、及びユーザー情報の取得
    :return: レンダリング対象のhtmlファイル'dailyreport/task_list.html'、およびhtmlファイル中で利用する日付で絞り込んだフォーム
    """
    dictionary = init_dictionary(request=request)
    dictionary.update(task_search_form=TaskSearchForm(request.GET))

    dictionary.update(task_form=get_narrowing_task(request=request))
    return render_to_response('dailyreport/task_list.html', dictionary, context_instance=RequestContext(request))


def delete_daily(request, daily_id):
    u"""日報削除(D)
        日報の削除を行います
        日報の投稿ユーザーでないユーザーがアクセスした場合、ログインページにリダイレクトされます
        正常に削除できた場合は（ユーザーの）日報一覧画面へリダイレクトされます
    :param request:ユーザー情報の取得
    :param daily_id:削除対象日報id
    :return:日報一覧ページへリダイレクト
    """
    if delete_daily_record(request, get_or_create_daily(request.user, daily_id)):
        return redirect('dailyreport:view_user_daily', user_id=request.user.id)   # 一覧画面にリダイレクト
    else:
        return redirect('login')


def search_daily_by_keyword(request):
    u"""日報検索
        日報をキーワードによって検索します
        検索条件
        ・キーワード数：1(複数キーワードのor対応,and未対応)
        ・検索対象：ユーザー名/日報タイトル/日報本文(y/w/t)
    :param request: 検索キーワードの取得
    :return: 絞り込んだ日報の一覧をdaily_list.htmlを利用してレンダリングする
    """
    dictionary = init_dictionary(request=request)
    dictionary.update(task_form=create_task_form_in_queryset(
        get_task_from_implement_date(request.user, timezone.now().date())
    ))
    dictionary.update(task_form_next=create_task_form_in_queryset(
        get_next_task(request.user, timezone.now().date())
    ))

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid() and form.cleaned_data['keyword'] is not '':
            queries = [Q(user__first_name__contains=word) |
                       Q(user__last_name__contains=word) |
                       Q(title__contains=word) |
                       Q(report_y__contains=word) |
                       Q(report_w__contains=word) |
                       Q(report_t__contains=word) for word in form.cleaned_data['keyword'].split()]
            query = queries.pop()
            for item in queries:
                query |= item
            dictionary.update(dailys=Daily.objects.filter(release=True).filter(query).order_by('-create_date'))
            dictionary.update(search_form=form)
            dictionary.update(keyword=form.cleaned_data['keyword'])
            dictionary.update(is_paginated=False)
            return render_to_response(
                'dailyreport/daily_list.html', dictionary, context_instance=RequestContext(request))

        return redirect('dailyreport:view_daily_list')


def user_daily_view(request, user_id):
    u"""ユーザー情報
        ユーザーごとの投稿情報を表示します
        表示対象：
            各ユーザーが投稿した日報
            (自分のページの場合)非公開状態の日報
        その他の表示内容は日報一覧と同様です
    :param request: ユーザー情報の取得
    :param user_id: 表示対象ユーザーid
    :return: ユーザーで絞り込んだ日報のリストを日報一覧と同様のhtmlファイルを使用してレンダリングします
    """
    dictionary = init_dictionary(request=request)
    dictionary.update(daily_release_form=DailySearchForm(request.GET))
    dictionary.update(pages=create_pagination(
        request, get_user_daily_list(request=request, user=user_id)))
    dictionary.update(dailys=dictionary['pages'].object_list)
    dictionary.update(is_paginated=True)
    dictionary.update(task_form=create_task_form_in_queryset(
        get_task_from_implement_date(request.user, timezone.now().date())
    ))
    dictionary.update(task_form_next=create_task_form_in_queryset(
        get_next_task(request.user, timezone.now().date())
    ))
    dictionary.update(userinfo=get_object_or_404(auth.get_user_model(), pk=user_id))

    return render_to_response('dailyreport/daily_list.html', dictionary, context_instance=RequestContext(request))


def user_list_view(request):
    u"""ユーザー一覧
        登録しているユーザー全員を表示
    :param request:初期情報
    :return:ユーザーの一覧とユーザー検索フォーム
    """
    dictionary = init_dictionary(request=request)
    dictionary.update(users=User.objects.all().order_by('first_name'))
    dictionary.update(user_search_form=SearchForm())

    return render_to_response('dailyreport/user_list.html', dictionary, context_instance=RequestContext(request))


def search_user_by_keyword(request):
    u"""ユーザー検索
        ユーザーをキーワード検索
        検索対象：
            username, first_name, last_name
        :param request:検索リクエスト
        :return:検索結果ユーザー一覧とユーザー検索フォーム
    """
    dictionary = init_dictionary(request=request)
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            dictionary.update(users=User.objects.all().filter(
                Q(username__contains=form.cleaned_data['keyword']) |
                Q(first_name__contains=form.cleaned_data['keyword']) |
                Q(last_name__contains=form.cleaned_data['keyword'])).order_by('first_name'))
            dictionary.update(user_search_form=form)

            return render_to_response(
                'dailyreport/user_list.html', dictionary, context_instance=RequestContext(request))
    else:
        dictionary.update(users=User.objects.all().order_by('id'))
        dictionary.update(user_search_form=SearchForm())

    return render_to_response('dailyreport/user_list.html', dictionary, context_instance=RequestContext(request))


def comment_edit_view(request, daily_id, comment_id=None):
    u"""コメント編集
        コメントの編集/新規作成を行います
    :param request:
    :param daily_id:コメントが投稿されている日報のid
    :param comment_id:(編集の場合)編集対象のコメントのid
    :return:編集されたコメントの投稿されている日報詳細/コメント編集フォーム(編集失敗の場合)
    """
    dictionary = init_dictionary(request=request)
    dictionary.update(daily=get_or_create_daily(daily_id=daily_id))
    dictionary.update(comment=get_or_create_comment(user=request.user, comment_id=comment_id))
    if request.user != dictionary['comment'].user:
        return redirect('login')
    flag, dictionary['comment_form'] = edit_comment(request, dictionary['daily'], dictionary['comment'])

    if request.method == 'POST' and flag:
        return redirect('dailyreport:view_daily_detail', daily_id=dictionary['daily'].id)
    elif flag is False:
        return render_to_response('dailyreport/comment_edit.html', dictionary, context_instance=RequestContext(request))

    return render_to_response('dailyreport/comment_edit.html', dictionary, context_instance=RequestContext(request))


def delete_comment(request, daily_id, comment_id):
    u"""コメントの削除
        コメントを削除します
    :param request:
    :param daily_id:リダイレクト先日報id
    :param comment_id:削除対象コメントid
    :return:
    """
    delete_comment_record(request, get_or_create_comment(request.user, comment_id))
    return redirect('dailyreport:view_daily_detail', daily_id=daily_id)
