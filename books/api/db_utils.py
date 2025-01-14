from django.db import connection


def info_dict(query, list_of_args):
    with connection.cursor() as cursor:
        cursor.execute(query, list_of_args)
        results = cursor.fetchall()
        data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]

    return data


class BookManagementDBUtils:

    @classmethod
    def get_book_detail(cls, book_id):
        query = """
                SELECT
                    b.id as book_id,
                    b.bookname,
                    u.publicationsname as publisher,
                    b.authorname,
                    b.translatorname,
                    b.releaseddate,
                    b.bookcoverimage,
                    b.price,
                    b.description,
                    b.numberofpages,
                    l.name as language,
                    bf.bookdemofile
                FROM books b
                INNER JOIN users u ON u.id = b.userid
                INNER JOIN languages l ON b.languageid = l.id
                INNER JOIN bookfiles bf ON b.id = bf.bookid
                WHERE b.id = %s
                """
        return info_dict(query=query, list_of_args=[book_id])

    @classmethod
    def get_book_review_counts(cls, book_id):
        query = """
            SELECT
                ROUND(COALESCE(AVG(r.rating), 0), 1) as reviewaverage,
                COALESCE(COUNT(r.rating), 0) as reviewcount
            FROM books b
            INNER JOIN (
                SELECT
                    bookid,
                    rating
                FROM reviews
            ) r ON b.id = r.bookid
            WHERE b.id = %s
            GROUP BY
                b.id;
        """
        return info_dict(query=query, list_of_args=[book_id])


    @classmethod
    def get_book_categories(cls, book_id):
        query = """
            SELECT
                c.name as category_name
            FROM books b
            INNER JOIN bookcategories bc ON b.id = bc.bookid
            INNER JOIN categories c ON bc.categoryid = c.id
            WHERE b.id = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [book_id])
            results = cursor.fetchall()
            return results

