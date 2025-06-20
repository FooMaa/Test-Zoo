from rest_framework import serializers

from .models import Animal, Section, Procedure


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(),
        source='section',
        write_only=True,
        required=True
    )

    class Meta:
        model = Animal
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['section'] = {
            'id': instance.section.id,
            'name': instance.section.name,
        }
        return representation


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'
        extra_kwargs = {
            'animal': {'required': False}
        }
        read_only_fields = ('datetime',)

    def validate(self, data):
        if 'animal' not in data and 'pk' not in self.context:
            raise serializers.ValidationError({
                'animal': 'Animal must be specified either in URL or request data'
            })
        return data
