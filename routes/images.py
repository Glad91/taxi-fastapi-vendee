from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response
from PIL import Image, ExifTags
import io
from urllib.parse import quote

router = APIRouter()


@router.post("/compresser-image", summary="Compression d'image au format WebP")
async def compresser_image(
    fichier: UploadFile = File(..., description="Image à compresser (JPEG, PNG, etc.)"),
    qualite: int = 80
):
    """
    Compresse une image au format WebP pour un meilleur gain de place.

    - **fichier**: L'image à compresser (formats supportés: JPEG, PNG, BMP, TIFF, etc.)
    - **qualite**: Qualité de compression WebP (1-100, défaut: 80). Plus la valeur est élevée, meilleure est la qualité mais plus le fichier est lourd.

    Retourne l'image compressée au format WebP.
    """
    # Validation de la qualité
    if not 1 <= qualite <= 100:
        raise HTTPException(
            status_code=400,
            detail="La qualité doit être comprise entre 1 et 100"
        )

    # Vérification du type de fichier
    if not fichier.content_type or not fichier.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être une image"
        )

    try:
        # Lecture de l'image
        contenu = await fichier.read()
        image = Image.open(io.BytesIO(contenu))

        # Corriger l'orientation EXIF si présente
        try:
            # Chercher la balise d'orientation dans les données EXIF
            exif = image.getexif()
            if exif:
                # Trouver le code de la balise Orientation
                orientation_key = None
                for key, val in ExifTags.TAGS.items():
                    if val == 'Orientation':
                        orientation_key = key
                        break

                if orientation_key and orientation_key in exif:
                    orientation = exif[orientation_key]

                    # Appliquer la rotation selon la valeur d'orientation
                    if orientation == 3:
                        image = image.rotate(180, expand=True)
                    elif orientation == 6:
                        image = image.rotate(270, expand=True)
                    elif orientation == 8:
                        image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Pas de données EXIF ou orientation, continuer normalement
            pass

        # Conversion en RGB si nécessaire (WebP ne supporte pas certains modes)
        if image.mode in ("RGBA", "LA", "P"):
            # Créer un fond blanc pour les images avec transparence
            fond = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            fond.paste(image, mask=image.split()[-1] if image.mode in ("RGBA", "LA") else None)
            image = fond
        elif image.mode != "RGB":
            image = image.convert("RGB")

        # Compression en WebP
        tampon = io.BytesIO()
        image.save(tampon, format="WEBP", quality=qualite, method=6)
        tampon.seek(0)

        # Calcul de la réduction de taille
        taille_originale = len(contenu)
        taille_compressee = len(tampon.getvalue())
        reduction_pourcentage = ((taille_originale - taille_compressee) / taille_originale) * 100

        # Préparer le nom de fichier encodé pour le header Content-Disposition
        nom_base = fichier.filename.rsplit('.', 1)[0] if fichier.filename else "image"
        nom_fichier_encode = quote(f"{nom_base}.webp")

        # Retour de l'image compressée avec des en-têtes informatifs
        return Response(
            content=tampon.getvalue(),
            media_type="image/webp",
            headers={
                "X-Original-Size": str(taille_originale),
                "X-Compressed-Size": str(taille_compressee),
                "X-Reduction-Percentage": f"{reduction_pourcentage:.2f}",
                "Content-Disposition": f"attachment; filename*=UTF-8''{nom_fichier_encode}"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la compression de l'image: {str(e)}"
        )