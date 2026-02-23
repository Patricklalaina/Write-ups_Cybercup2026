import hashlib

# Premier de Mersenne M521
p = 2**521 - 1

# Les 5 stations complètes (hauts de l'île)
complete_shares = [
    (1, 0xd0393fd5aa76c02f53757a5883d97a0f0ade112cffc590c8378f2b5a6696a284dcc1ef10c29f7275958952bca3c40922f75258f47e808d587aca867f48f0d798f5),
    (2, 0xa0deb8650c459c78e99ca5ae29c1399c8221723e6c966a4a4494ec69bcb20399336bba13c10998b4b0b554cffdaec9b8b536e6fa9ea4eefa7321782797b84672e4),
    (3, 0x9dc6d639cbda2c6893efafe086027e1f9126a9e27f2d342e45e8090675c2eca7e4ae330b163f8f059fa665a20ea4be41a4de9fe882ac3b08387ba8649622293745),
    (4, 0xff3a80c762b7a71ee3793ed87a7951f819960a86b067cefbe94cac78b9f556291ebf42ae21395da1a5e9d3d426624b6cf5bebb4487d9311737417749e401c0cb57),
    (5, 0x748755843bdf0733e28882bb8f096fdd4c4ae2142cba5fb2ea4ba7e65a7b007a75f34a4f7a94b4b8e5b9d425d415b5750066cb52e451f11933b086614b816d4ecb)
]

# Station 6 (côtière inondée - 20 bits manquants)
y6_partial = 0x18e91e304d2372e99ce65481f4a15284c423aa9ac47a25b639109b2c0c5d60cb6ba133679b80d2d34cfdc2c2968c5b83977eaa1b6e5ad7ed0368e3d0a9639300000

def lagrange_interpolation(shares, x_target, prime):
    """
    Interpolation de Lagrange pour reconstruire le polynôme
    et l'évaluer en x_target
    """
    result = 0
    
    for i, (xi, yi) in enumerate(shares):
        # Calcul du coefficient de Lagrange L_i(x_target)
        numerator = 1
        denominator = 1
        
        for j, (xj, yj) in enumerate(shares):
            if i != j:
                numerator = (numerator * (x_target - xj)) % prime
                denominator = (denominator * (xi - xj)) % prime
        
        # L_i(x_target) = numerator / denominator (mod p)
        lagrange_coef = (numerator * pow(denominator, -1, prime)) % prime
        
        # P(x_target) += y_i * L_i(x_target)
        result = (result + yi * lagrange_coef) % prime
    
    return result

def secret_to_ascii(secret):
    """Convertir le secret (entier) en chaîne ASCII"""
    try:
        secret_hex = hex(secret)[2:].rstrip('L')
        # Assurer un nombre pair de caractères hex
        if len(secret_hex) % 2:
            secret_hex = '0' + secret_hex
        secret_bytes = bytes.fromhex(secret_hex)
        return secret_bytes.decode('ascii', errors='ignore')
    except:
        return None

def solve():
    """Résolution par force brute sur les 20 bits manquants"""
    print("Eye of the Storm - Résolution")
    print("=" * 70)
    print(f"Recherche parmi 2^20 = {2**20:,} possibilités...\n")
    
    for missing_bits in range(1 << 20):
        if missing_bits % 50000 == 0:
            progress = (missing_bits / (1 << 20)) * 100
            print(f"Progression: {progress:.1f}% ({missing_bits:,} / 1,048,576)", end='\r')
        
        # Reconstruire y_6 complet
        y6_reconstructed = y6_partial | missing_bits
        
        # Créer les 6 parts nécessaires
        shares_6 = complete_shares + [(6, y6_reconstructed)]
        
        # Interpoler le secret (valeur à x=0)
        secret = lagrange_interpolation(shares_6, 0, p)
        
        # Convertir en ASCII
        flag = secret_to_ascii(secret)
        
        if flag:
            # Vérifier le format et le hash
            if flag.startswith('CCOI26{') and flag.endswith('}'):
                hash_result = hashlib.sha256(flag.encode()).hexdigest()[:16]
                
                if hash_result == "f687cb74fdcefefc":
                    print(f"\n\nFLAG TROUVÉ !")
                    print("=" * 70)
                    print(f"Bits manquants: {missing_bits} (0x{missing_bits:05x})")
                    print(f"Secret (hex): {hex(secret)}")
                    print(f"Flag: {flag}")
                    print(f"SHA256[:16]: {hash_result}")
                    print("=" * 70)
                    return flag
    
    print("\nAucune solution trouvée")
    return None

if __name__ == "__main__":
    solve()
