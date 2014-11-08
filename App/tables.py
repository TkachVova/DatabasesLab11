import django_tables2 as tables
from django_tables2.utils import A


class CarTable(tables.Table):
    id = tables.LinkColumn('car_detail', args=[A('id')])
    producer = tables.Column()
    model = tables.Column()
    car_class = tables.Column(verbose_name='class')
    drive = tables.Column()
    #engine = tables.Column()
    #interior = tables.Column()
    #body = tables.Column()
    cost = tables.Column()
    #selected = tables.CheckBoxColumn(accessor='id')
    selection = tables.CheckBoxColumn(accessor='id', attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False)
    class Meta:
        attrs = {"class": "paleblue"}
