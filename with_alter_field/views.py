from django.shortcuts import render

from with_alter_field.models import AlterField


def alter_field(request):
    all_alter = AlterField.objects.all()
    main_alter = all_alter.filter(is_main=True)
    other_alter = all_alter.filter(is_main=False)
    if main_alter:
        new_other = main_alter[0]
        if request.method == 'POST':
            if 'other_user' in request.POST:
                new_main = other_alter.get(pk=request.POST['other_user'])
                print(request.POST['other_user'])
                new_other.is_main = False
                new_main.is_main = True
                new_other.save()
                new_main.save()
                main_alter = all_alter.filter(is_main=True)
                other_alter = all_alter.filter(is_main=False)
    context = {'main_alter': main_alter, 'other_alter': other_alter}
    return render(request, 'with_alter_field.html', context)
