import re
import math
import inspect

# ---------------------------------------------
# Fizik Formülleri Sınıfları (Kategori Bazlı)
# ---------------------------------------------

class FizikFormulleri:

    class Mekanik:
        @staticmethod
        def kuvvet(m: float, a: float) -> float:
            """F = m * a"""
            return m * a

        @staticmethod
        def kinetik_enerji(m: float, v: float) -> float:
            """Ek = 0.5 * m * v^2"""
            return 0.5 * m * v**2

        @staticmethod
        def potansiyel_enerji(m: float, g: float, h: float) -> float:
            """Ep = m * g * h"""
            return m * g * h

        @staticmethod
        def momentum(m: float, v: float) -> float:
            """p = m * v"""
            return m * v

        @staticmethod
        def hareket_hizi(u: float, a: float, t: float) -> float:
            """v = u + a * t"""
            return u + a * t

        @staticmethod
        def konum(u: float, a: float, t: float) -> float:
            """s = u * t + 0.5 * a * t^2"""
            return u * t + 0.5 * a * t**2

        @staticmethod
        def guc(W: float, t: float) -> float:
            """P = W / t"""
            if t == 0:
                raise ValueError("Zaman sıfır olamaz.")
            return W / t

        @staticmethod
        def merkezcil_kuvvet(m: float, v: float, r: float) -> float:
            """Fc = m * v^2 / r"""
            if r == 0:
                raise ValueError("Yarıçap sıfır olamaz.")
            return m * v**2 / r

        @staticmethod
        def yukselme_hizi(m: float, A: float, F: float, t: float) -> float:
            """
            Basit bir örnek: (örnek olarak)
            Yükselme hızı = Kuvvet / (kütle * alan) * zaman (varsayımsal)
            """
            if m == 0 or A == 0:
                raise ValueError("Kütle ve alan sıfır olamaz.")
            return (F / (m * A)) * t

    class Elektrik:
        @staticmethod
        def ohm_yasasi(V: float, R: float) -> float:
            """I = V / R"""
            if R == 0:
                raise ValueError("Direnç sıfır olamaz.")
            return V / R

        @staticmethod
        def elektrik_gucu(V: float, I: float) -> float:
            """P = V * I"""
            return V * I

        @staticmethod
        def direncteki_guc(R: float, I: float) -> float:
            """P = R * I^2"""
            return R * I**2

        @staticmethod
        def enerji(P: float, t: float) -> float:
            """E = P * t"""
            return P * t

        @staticmethod
        def kondansator_enerjisi(C: float, V: float) -> float:
            """E = 0.5 * C * V^2"""
            return 0.5 * C * V**2

        @staticmethod
        def kapasite(Q: float, V: float) -> float:
            """C = Q / V"""
            if V == 0:
                raise ValueError("Gerilim sıfır olamaz.")
            return Q / V

    class Termodinamik:
        @staticmethod
        def isi(m: float, c: float, deltaT: float) -> float:
            """Q = m * c * ΔT"""
            return m * c * deltaT

        @staticmethod
        def ideal_gaz(P: float, V: float, n: float, T: float) -> float:
            """PV = nRT -> R = PV / nT"""
            if n == 0 or T == 0:
                raise ValueError("Mol sayısı ve sıcaklık sıfır olamaz.")
            R = (P * V) / (n * T)
            return R

        @staticmethod
        def calisma(P: float, deltaV: float) -> float:
            """W = P * ΔV"""
            return P * deltaV

        @staticmethod
        def basinc(yukseklik: float, siklik: float = 1000, g: float = 9.81) -> float:
            """Basınç hesaplama: P = ρ g h"""
            return siklik * g * yukseklik

    class Optik:
        @staticmethod
        def mercek_gucu(f: float) -> float:
            """D = 1 / f"""
            if f == 0:
                raise ValueError("Odak uzaklığı sıfır olamaz.")
            return 1 / f

        @staticmethod
        def buyutme(di: float, do_: float) -> float:
            """B = di / do"""
            if do_ == 0:
                raise ValueError("Nesne uzaklığı sıfır olamaz.")
            return di / do_

        @staticmethod
        def refleksiyon_acisi(aci_gelis: float) -> float:
            """Yansıma açısı = geliş açısı"""
            return aci_gelis

        @staticmethod
        def kirmac_acisi(n1: float, n2: float, aci_gelis: float) -> float:
            """Snell Yasası: n1 sinθ1 = n2 sinθ2"""
            # açı derece ise radiana çevir
            rad = math.radians(aci_gelis)
            sin_theta2 = (n1 / n2) * math.sin(rad)
            if abs(sin_theta2) > 1:
                raise ValueError("Tam yansıma gerçekleşiyor, kırılma yok.")
            theta2 = math.asin(sin_theta2)
            return math.degrees(theta2)

    class ModernFizik:
        @staticmethod
        def enerji_masif(m: float, c: float = 3e8) -> float:
            """E = m * c^2"""
            return m * c**2

        @staticmethod
        def foton_enerjisi(frekans: float, h: float = 6.626e-34) -> float:
            """E = h * f"""
            return h * frekans

        @staticmethod
        def de_broglie_boyu(m: float, v: float, h: float = 6.626e-34) -> float:
            """λ = h / (m * v)"""
            if m == 0 or v == 0:
                raise ValueError("Kütle ve hız sıfır olamaz.")
            return h / (m * v)

# ---------------------------------------------
# Ana Soru Çözücü Sınıfı
# ---------------------------------------------

class FizikSoruCozucu:
    def __init__(self):
        # Formülleri kategori + fonksiyon adı ile eşleştir
        # Anahtar kelimeler burada çok önemli
        self.formul_map = {
            # Mekanik
            "kuvvet": ("mekanik", "kuvvet"),
            "kinetik enerji": ("mekanik", "kinetik_enerji"),
            "potansiyel enerji": ("mekanik", "potansiyel_enerji"),
            "momentum": ("mekanik", "momentum"),
            "hareket hızı": ("mekanik", "hareket_hizi"),
            "konum": ("mekanik", "konum"),
            "güç": ("mekanik", "guc"),
            "merkezcil kuvvet": ("mekanik", "merkezcil_kuvvet"),
            "yükselme hızı": ("mekanik", "yukselme_hizi"),
            # Elektrik
            "ohm": ("elektrik", "ohm_yasasi"),
            "elektrik gücü": ("elektrik", "elektrik_gucu"),
            "direnç gücü": ("elektrik", "direncteki_guc"),
            "enerji elektrik": ("elektrik", "enerji"),
            "kondansator enerjisi": ("elektrik", "kondansator_enerjisi"),
            "kapasite": ("elektrik", "kapasite"),
            # Termodinamik
            "ısı": ("termodinamik", "isi"),
            "ideal gaz": ("termodinamik", "ideal_gaz"),
            "çalışma": ("termodinamik", "calisma"),
            "basınç": ("termodinamik", "basinc"),
            # Optik
            "mercek gücü": ("optik", "mercek_gucu"),
            "büyütme": ("optik", "buyutme"),
            "yansıma açısı": ("optik", "refleksiyon_acisi"),
            "kırılma açısı": ("optik", "kirmac_acisi"),
            # Modern Fizik
            "enerji kütle": ("modernfizik", "enerji_masif"),
            "foton enerjisi": ("modernfizik", "foton_enerjisi"),
            "de broglie": ("modernfizik", "de_broglie_boyu"),
        }

    def _sayilari_bul(self, metin: str):
        """
        Metindeki sayı ve ondalıklı sayıları yakalar
        - İşaretli sayıları ve ondalıklı sayıları yakalar
        """
        sayilar = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", metin)
        return [float(s) for s in sayilar]

    def _anahtar_kelime_bul(self, soru: str):
        soru = soru.lower()
        # Anahtar kelimeleri uzunluktan kısaya sırala (ör: "kinetik enerji" önce yakalansın)
        for kelime in sorted(self.formul_map.keys(), key=len, reverse=True):
            if kelime in soru:
                return self.formul_map[kelime]
        return None

    def soru_coz(self, soru: str):
        formül_bilgisi = self._anahtar_kelime_bul(soru)
        if not formül_bilgisi:
            return "Maalesef soruyu anlayamadım. Lütfen daha açık sorun."

        kategori, fonksiyon_adi = formül_bilgisi
        formül_kategori = getattr(FizikFormulleri, kategori.capitalize(), None)
        if formül_kategori is None:
            return "Formül kategorisi bulunamadı."

        fonksiyon = getattr(formül_kategori, fonksiyon_adi, None)
        if fonksiyon is None:
            return "Formül fonksiyonu bulunamadı."

        parametreler = self._sayilari_bul(soru)
        n_param = len(inspect.signature(fonksiyon).parameters)

        if len(parametreler) < n_param:
            return f"Bu soru için yeterli bilgi yok. {n_param} parametre gerekli, siz {len(parametreler)} verdiniz."

        parametreler = parametreler[:n_param]

        try:
            sonuc = fonksiyon(*parametreler)
            if isinstance(sonuc, bool):
                return f"Sonuç: {sonuc}"
            elif isinstance(sonuc, float):
                return f"Sonuç: {sonuc:.6g}"
            else:
                return f"Sonuç: {sonuc}"
        except Exception as e:
            return f"Hesaplama sırasında hata oluştu: {str(e)}"


# ---------------------------------------------
# Ana Program Döngüsü
# ---------------------------------------------

def main():
    print("Gelişmiş Fizik Formülleri Soru Çözücüye Hoş Geldiniz!")
    print("Soru sorabilirsiniz. Örnek: '10 kg kütleli cisme 5 m/s² ivme uygulanırsa kuvvet nedir?'")
    print("Çıkmak için 'çıkış' yazınız.\n")

    cozucu = FizikSoruCozucu()

    while True:
        soru = input("Soru > ").strip()
        if soru.lower() in ["çıkış", "exit", "quit"]:
            print("Programdan çıkılıyor. İyi çalışmalar!")
            break
        cevap = cozucu.soru_coz(soru)
        print(cevap)
        print("-" * 50)


if __name__ == "__main__":
    main()
