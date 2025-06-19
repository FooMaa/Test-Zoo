from rest_framework import serializers
from .models import Animal, Section, Procedure


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    section = SectionSerializer(read_only=True)
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(),
        source='section',
        write_only=True,
        required=False
    )

    class Meta:
        model = Animal
        fields = '__all__'


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'
        extra_kwargs = {
            'animal': {'required': False}  # Делаем поле необязательным в запросе
        }
        read_only_fields = ('datetime',)

    def validate(self, data):
        if 'animal' not in data and 'animal_pk' not in self.context:
            raise serializers.ValidationError({
                'animal': 'Animal must be specified either in URL or request data'
            })
        return data