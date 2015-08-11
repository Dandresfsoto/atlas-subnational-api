from flask import jsonify
import marshmallow as ma

from atlas_core.helpers.flask import APIError


def marshal(schema, data, json=True, many=True):
    """Shortcut to marshals a marshmallow schema and dump out a flask json
    response, or raise an APIError with appropriate messages otherwise."""

    try:
        serialization_result = schema.dump(data, many=many)
    except ma.ValidationError as err:
        raise APIError(message=err.messages)

    if json:
        return jsonify(data=serialization_result.data)
    else:
        return serialization_result.data


XPY_FIELDS = ("import_value", "export_value", "export_rca", "distance", "cog",
              "coi", "product_id", "year")


class CountryProductYearSchema(ma.Schema):

    country_id = ma.fields.Constant(0)
    import_value = ma.fields.Constant(None)
    export_rca = ma.fields.Constant(None)
    distance = ma.fields.Constant(None)
    cog = ma.fields.Constant(None)
    coi = ma.fields.Constant(None)

    class Meta:
        fields = XPY_FIELDS + ("country_id", )


class DepartmentProductYearSchema(ma.Schema):

    class Meta:
        fields = XPY_FIELDS + ("department_id", )


class MunicipalityProductYearSchema(ma.Schema):

    class Meta:
        fields = XPY_FIELDS + ("municipality_id", )


class CountryMunicipalityProductYearSchema(ma.Schema):

    class Meta:
        fields = ("export_value", "country_id", "municipality_id",
                  "product_id", "year")


class CountryDepartmentProductYearSchema(ma.Schema):

    class Meta:
        fields = ("export_value", "country_id", "department_id",
                  "product_id", "year")


class DepartmentIndustryYearSchema(ma.Schema):

    class Meta:
        fields = ("employment", "wages", "rca", "distance", "cog", "coi",
                  "department_id", "industry_id", "year")


class MunicipalityIndustryYearSchema(ma.Schema):

    class Meta:
        fields = ("employment", "wages", "rca", "distance", "cog", "coi",
                  "municipality_id", "industry_id", "year")


class DepartmentSchema(ma.Schema):

    class Meta:
        fields = ("code", "id", "name", "population", "gdp")


class ProductYearSchema(ma.Schema):

    class Meta:
        fields = ("pci", "product_id", "year")


class IndustryYearSchema(ma.Schema):

    class Meta:
        fields = ("complexity", "employment", "wages", "num_establishments",
                  "industry_id", "year")


class DepartmentYearSchema(ma.Schema):

    class Meta:
        fields = ("department_id", "year", "eci", "diversity", "gdp_nominal",
                  "gdp_real", "gdp_pc_nominal", "gdp_pc_real", "population")


class MetadataSchema(ma.Schema):
    """Base serialization schema for metadata APIs."""

    class Meta:
        additional = ("id", "code", "level", "parent_id")


class ColombiaMetadataSchema(MetadataSchema):

    name_en = ma.fields.Str(required=False)
    name_short_en = ma.fields.Str(required=False)
    description_en = ma.fields.Str(required=False)

    name_es = ma.fields.Str(required=False)
    name_short_es = ma.fields.Str(required=False)
    description_es = ma.fields.Str(required=False)


country_product_year = CountryProductYearSchema(many=True)
department_product_year = DepartmentProductYearSchema(many=True)
municipality_product_year = MunicipalityProductYearSchema(many=True)
country_municipality_product_year = CountryMunicipalityProductYearSchema(many=True)
country_department_product_year = CountryDepartmentProductYearSchema(many=True)
department_industry_year = DepartmentIndustryYearSchema(many=True)
municipality_industry_year = MunicipalityIndustryYearSchema(many=True)
product_year = ProductYearSchema(many=True)
industry_year = IndustryYearSchema(many=True)
department_year = DepartmentYearSchema(many=True)
department = DepartmentSchema(many=True)
metadata = ColombiaMetadataSchema(many=True)
