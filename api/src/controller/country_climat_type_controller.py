"""
Module Flask pour la gestion des types de climat.
Ce module fournit une API REST permettant de récupérer, créer, mettre à jour et supprimer des types de climat
associés à des pays.

Dépendances :
- Flask
- Flask-RESTx
- psycopg2 (pour la connexion à la base de données PostgreSQL)
"""

from flask import Blueprint, jsonify, request
from flask_restx import Resource, fields, Namespace
import psycopg2.extras
from connect_db import DBConnection


country_climat_type_controller = Blueprint('country_climat_type_controller', __name__)

country_climat_type_namespace = Namespace('country_climat_type', description='Gestion des types de climat')

documentation_model = country_climat_type_namespace.model('CountryClimatType', {
    'id_climat_type': fields.Integer(readonly=True, description='Identifiant unique du type de climat'),
    'id_country': fields.Integer(readonly=True, description='Identifiant du pays associé'),
    'name': fields.String(required=True, description='Nom du type de climat'),
    'description': fields.String(description='Description du type de climat')
})

@country_climat_type_controller.route('/country_climat_types', methods=['GET'])
def get_all_climat_types():
    """Récupère tous les types de climat disponibles dans la base de données."""
    try:
        with DBConnection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM country_climat_type")
            country_climat_types = cursor.fetchall()
            return country_climat_types, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_climat_type_controller.route('/country_climat_type/<int:climat_type_id>', methods=['GET'])
def get_climat_type_by_id(climat_type_id):
    """Récupère un type de climat spécifique par son identifiant."""
    try:
        with DBConnection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM country_climat_type WHERE id_climat_type = %s", (climat_type_id,))
            country_climat_type = cursor.fetchone()
            if not country_climat_type:
                return jsonify({"error": "Climat type not found"}), 404
            return country_climat_type, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_climat_type_controller.route('/country_climat_type', methods=['POST'])
def create_climat_type():
    """Crée un nouveau type de climat et l'ajoute à la base de données."""
    try:
        data = request.json
        if "name" not in data:
            return jsonify({"error": "Missing 'name'"}), 400

        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO country_climat_type (name, description)
                VALUES (%s, %s) RETURNING id_climat_type
                """,
                (data["name"], data.get("description"))
            )
            new_id = cursor.fetchone()[0]
            conn.commit()

        return jsonify({
            "id_climat_type": new_id,
            "name": data["name"],
            "description": data.get("description")
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_climat_type_controller.route('/country_climat_type/<int:climat_type_id>', methods=['PUT'])
def update_climat_type(climat_type_id):
    """Met à jour les informations d'un type de climat existant."""
    try:
        data = request.json
        if "name" not in data:
            return jsonify({"error": "Missing 'name'"}), 400

        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE country_climat_type
                SET name = %s, description = %s
                WHERE id_climat_type = %s
                RETURNING id_climat_type
                """,
                (data["name"], data.get("description"), climat_type_id)
            )
            updated = cursor.fetchone()
            conn.commit()

            if not updated:
                return jsonify({"error": "Climat type not found"}), 404
            return jsonify({"message": "Climat type updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_climat_type_controller.route('/country_climat_type/<int:climat_type_id>', methods=['DELETE'])
def delete_climat_type(climat_type_id):
    """Supprime un type de climat de la base de données."""
    try:
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM country_climat_type WHERE id_climat_type = %s RETURNING id_climat_type",
                (climat_type_id,)
            )
            deleted = cursor.fetchone()
            conn.commit()

            if not deleted:
                return jsonify({"error": "Climat type not found"}), 404
            return jsonify({"message": "Climat type deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_climat_type_namespace.route('/country_climat_types')
class ClimatTypes(Resource):
    """Ressource permettant de gérer la récupération de tous les types de climat."""
    @country_climat_type_namespace.doc(description="Récupère tous les types de climat.")
    @country_climat_type_namespace.marshal_list_with(documentation_model)
    def get(self):
        """
        Récupère la liste de tous les types de climat.

        :return: Une liste des types de climat en JSON avec un code de statut 200 si réussi,
                 ou une erreur avec un code de statut approprié en cas d'échec.
        """
        return get_all_climat_types()[0]

@country_climat_type_namespace.route('/country_climat_type/<int:climat_type_id>')
class ClimatTypeById(Resource):
    """Ressource permettant de gérer un type de climat spécifique par ID."""
    @country_climat_type_namespace.doc(description="Récupère un type de climat par ID.")
    @country_climat_type_namespace.marshal_with(documentation_model)
    def get(self, climat_type_id):
        """
        Récupère un type de climat spécifique à partir de son ID.

        :param climat_type_id: L'ID du type de climat à récupérer.
        :return: Les détails du type de climat en JSON avec un code de statut 200 si trouvé,
                 ou une erreur avec un code de statut 404 si non trouvé.
        """
        return get_climat_type_by_id(climat_type_id)[0]

    @country_climat_type_namespace.doc(description="Met à jour un type de climat.")
    @country_climat_type_namespace.expect(documentation_model)
    def put(self, climat_type_id):
        """
        Met à jour un type de climat spécifique à partir de son ID.

        :param climat_type_id: L'ID du type de climat à mettre à jour.
        :return: Les détails du type de climat mis à jour en JSON avec un code de statut 200 si réussi,
                 ou une erreur avec un code de statut 404 si le type de climat n'existe pas.
        """
        return update_climat_type(climat_type_id)[0]

    @country_climat_type_namespace.doc(description="Supprime un type de climat.")
    def delete(self, climat_type_id):
        """
        Supprime un type de climat spécifique à partir de son ID.

        :param climat_type_id: L'ID du type de climat à supprimer.
        :return: Un message de confirmation en JSON avec un code de statut 200 si réussi,
                 ou une erreur avec un code de statut 404 si le type de climat n'existe pas.
        """
        return delete_climat_type(climat_type_id)[0]
