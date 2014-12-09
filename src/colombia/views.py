from flask import request
from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from colombia.models import HSProduct
from colombia import ext


hs_product_fields = {
    'code': fields.String,
    'id': fields.String,
    'name': fields.String,
    'aggregation': fields.String,
}


class HSProductAPI(restful.Resource):

    @ext.cache.cached(timeout=60)
    @marshal_with(hs_product_fields)
    def get(self, code):
        """Get a :py:class:`~colombia.models.HSProduct` with the given code.

        :param code: See :py:class:`colombia.models.HSProduct.code`
        :type code: int
        :code 404: product doesn't exist
        """
        q = HSProduct.query.filter_by(code=code).first_or_abort(code)
        return q


class HSProductListAPI(restful.Resource):

    @marshal_with(hs_product_fields)
    def get(self):
        """Get a :py:class:`~colombia.models.HSProduct` with the given code.

        :param code: See :py:class:`colombia.models.HSProduct.code`
        :type code: int
        :query aggregation: :py:class:`colombia.models.HSProduct.aggregation`
        :code 404: product doesn't exist
        """

        q = HSProduct.query

        aggregation = request.args.get("aggregation", None)
        if aggregation is not None:
            if aggregation not in HSProduct.AGGREGATIONS:
                msg = "Expected one of: {0}, got {1}"\
                    .format(HSProduct.AGGREGATIONS, aggregation)
                restful.abort(400, message=msg)

            q = q.filter_by(aggregation=aggregation)

        return q.all()
