from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, List, Optional


# Clases
class Deportista(ABC):
    def __init__(self, nombre: str, edad: int, deporte: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not isinstance(edad, int) or edad <= 0:
            raise ValueError("La edad debe ser un número entero positivo.")
        if not deporte or not deporte.strip():
            raise ValueError("El deporte no puede estar vacío.")

        self.nombre = nombre.strip()
        self.edad = edad
        self.deporte = deporte.strip()

        self.__puntaje = 0
        self.__cantidad_de_competencias = 0

    @property
    def puntaje(self) -> int:
        return self.__puntaje

    @property
    def cantidad_de_competencias(self) -> int:
        return self.__cantidad_de_competencias

    @abstractmethod
    def obtener_informacion_basica(self) -> str:
        """Cada subclase debe redefinir este método (polimorfismo)."""

    def obtener_estadisticas(self) -> str:
        return (
            f"El deportista ha competido en {self.__cantidad_de_competencias} competencias "
            f"y cuenta con un total de {self.__puntaje} puntos."
        )

    def reiniciar_puntaje(self) -> None:
        self.__puntaje = 0
        self.__cantidad_de_competencias = 0

    def actualizar_puntaje_y_competencias(self, nuevo_puntaje: int) -> None:
        if not isinstance(nuevo_puntaje, int) or nuevo_puntaje <= 0:
            raise ValueError("El puntaje debe ser un número entero positivo.")
        self.__puntaje += nuevo_puntaje
        self.__cantidad_de_competencias += 1


class Registro:
    def __init__(self, deportistas: Optional[List[Deportista]] = None):
        self.deportistas: List[Deportista] = deportistas if deportistas is not None else []

    def _normalizar(self, texto: str) -> str:
        return texto.strip().lower()

    def obtener_deportista(self, nombre: str) -> Optional[Deportista]:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre para buscar no puede estar vacío.")

        nombre_norm = self._normalizar(nombre)
        for deportista in self.deportistas:
            if self._normalizar(deportista.nombre) == nombre_norm:
                return deportista
        return None

    def añadir_deportista(self, deportista: Deportista) -> bool:
        if deportista is None:
            raise ValueError("Debe proporcionar un deportista válido.")

        if self.obtener_deportista(deportista.nombre) is not None:
            raise ValueError(f"El deportista '{deportista.nombre}' ya se encuentra registrado.")

        self.deportistas.append(deportista)
        return True

    def mostrar_deportistas(self) -> None:
        for deportista in sorted(self.deportistas, key=lambda d: d.puntaje, reverse=True):
            print(
                f"Nombre: {deportista.nombre}, Deporte: {deportista.deporte}, "
                f"Puntaje: {deportista.puntaje}"
            )

    def mostrar_ranking_por_deporte(self, deporte: str) -> None:
        if not deporte or not deporte.strip():
            raise ValueError("El deporte no puede estar vacío.")
        deporte_norm = self._normalizar(deporte)

        deportistas_filtrados = [
            d for d in self.deportistas if self._normalizar(d.deporte) == deporte_norm
        ]
        for deportista in sorted(deportistas_filtrados, key=lambda d: d.puntaje, reverse=True):
            print(
                f"Nombre: {deportista.nombre}, Deporte: {deportista.deporte}, "
                f"Puntaje: {deportista.puntaje}"
            )

    def mostrar_n_mejores_deportistas(self, deporte: str, n: int) -> None:
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n debe ser un entero positivo.")

        if not deporte or not deporte.strip():
            raise ValueError("El deporte no puede estar vacío.")
        deporte_norm = self._normalizar(deporte)

        deportistas_filtrados = [
            d for d in self.deportistas if self._normalizar(d.deporte) == deporte_norm
        ]
        mejores_deportistas = sorted(
            deportistas_filtrados, key=lambda d: d.puntaje, reverse=True
        )[:n]
        for deportista in mejores_deportistas:
            print(
                f"Nombre: {deportista.nombre}, Deporte: {deportista.deporte}, "
                f"Puntaje: {deportista.puntaje}"
            )

    def buscar_deportista(self, nombre: str) -> str:
        deportista = self.obtener_deportista(nombre)
        if deportista is None:
            return f"El deportista '{nombre}' no fue encontrado."
        return (
            f"{deportista.obtener_informacion_basica()}\n"
            f"{deportista.obtener_estadisticas()}"
        )

class Competencia:
    def __init__(
        self,
        nombre: str,
        fecha: date,
        participantes: Optional[List[Deportista]],
        resultados: Optional[Dict[Deportista, int]],
        deporte: str,
        registro: Registro,
    ):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la competencia no puede estar vacío.")
        if not isinstance(fecha, date):
            raise ValueError("La fecha debe ser un objeto datetime.date.")
        if not deporte or not deporte.strip():
            raise ValueError("El deporte de la competencia no puede estar vacío.")
        if registro is None:
            raise ValueError("Debe proporcionar un registro válido.")

        self.nombre = nombre.strip()
        self.fecha = fecha
        self.participantes: List[Deportista] = participantes if participantes is not None else []
        self.resultados: Dict[Deportista, int] = resultados if resultados is not None else {}
        self.deporte = deporte.strip()
        self.registro = registro

    def inscribir_participante(self, deportista):
        if deportista is None:
            raise ValueError("Debe proporcionar un deportista válido.")

        deportista_encontrado = self.registro.obtener_deportista(deportista.nombre)
        if deportista_encontrado is None:
            raise ValueError(
                f"El deportista '{deportista.nombre}' no se encuentra registrado."
            )

        if deportista_encontrado.deporte.strip().lower() != self.deporte.strip().lower():
            raise ValueError(
                f"El deportista '{deportista.nombre}' no pertenece al deporte de la competencia."
            )

        if deportista_encontrado in self.participantes:
            raise ValueError(
                f"El deportista '{deportista.nombre}' ya está inscrito en la competencia."
            )

        self.participantes.append(deportista_encontrado)

    def registrar_resultado(self, resultado):
        if not isinstance(resultado, dict):
            raise ValueError("El resultado debe ser un diccionario {deportista: puntaje}.")

        for deportista, puntaje in resultado.items():
            if deportista not in self.participantes:
                raise ValueError(
                    f"El deportista '{deportista.nombre}' no está inscrito en la competencia."
                )
            if not isinstance(puntaje, int) or puntaje <= 0:
                raise ValueError(
                    f"El puntaje asignado a '{deportista.nombre}' debe ser un entero positivo."
                )

            deportista.actualizar_puntaje_y_competencias(puntaje)
            self.resultados[deportista] = puntaje

    def  mostrar_resultado(self):
        for deportista, puntaje in self.resultados.items():
            print(f"Nombre: {deportista.nombre}, Deporte: {deportista.deporte}, Puntaje: {puntaje}")

    def  mostrar_n_posiciones(self,n):
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n debe ser un entero positivo.")

        sorted_deportistas = sorted(
            self.resultados.keys(), key=lambda d: self.resultados[d], reverse=True
        )
        for i, deportista in enumerate(sorted_deportistas[:n], start=1):
            print(f"{i}. Nombre: {deportista.nombre}, Deporte: {deportista.deporte}, Puntaje: {self.resultados[deportista]}")

class Futbolista(Deportista):
    def __init__(self, nombre, edad, equipo, goles, asistencias, posicion):
        super().__init__(nombre, edad, "Fútbol")
        self.equipo = equipo
        self.goles = goles
        self.asistencias = asistencias
        self.posicion = posicion

    def obtener_informacion_basica(self):
        return f"El futbolista se llama {self.nombre}, juega en el equipo {self.equipo} y su posición es {self.posicion}."
    def añadir_goles(self, goles):
        if goles < 0:
            raise ValueError("La cantidad de goles debe ser un número entero positivo.")
        self.goles += goles
    def añadir_asistencias(self, asistencias):
        if asistencias < 0:
            raise ValueError("La cantidad de asistencias debe ser un número entero positivo.")
        self.asistencias += asistencias
    def calcular_rendimiento(self):
        if self.cantidad_de_competencias == 0:
            return 0
        rendimiento = (self.goles * 2 + self.asistencias * 0.7) / self.cantidad_de_competencias
        return rendimiento
    def cambiar_de_equipo(self, nuevo_equipo):
        self.equipo = nuevo_equipo
        self.reiniciar_puntaje()
    
class Tenista(Deportista):
    def __init__(self, nombre, edad, pareja, ranking_atp):
        super().__init__(nombre, edad, "Tenis")
        self.pareja = pareja
        self.ranking_atp = ranking_atp

    def obtener_informacion_basica(self):
        return f"El tenista se llama {self.nombre}, su pareja es {self.pareja} y su ranking ATP es {self.ranking_atp}."
    def actualizar_de_pareja(self, nueva_pareja):
        self.pareja = nueva_pareja
        self.reiniciar_puntaje()
    def actualizar_ranking(self,nueva_posicion):
        if nueva_posicion < 0:
            raise ValueError("La posición en el ranking no puede ser negativa.")
        self.ranking_atp = nueva_posicion
        self.reiniciar_puntaje()

class Atleta(Deportista):
    def __init__(self, nombre, edad, disciplina):
        super().__init__(nombre, edad, "Atletismo")
        self.disciplina = disciplina
        self.mejores_tiempos = []

    def obtener_informacion_basica(self):
        return f"El atleta se llama {self.nombre} y su disciplina es {self.disciplina}."
    def agregar_mejores_tiempos(self, tiempo):
        if tiempo <= 0:
            raise ValueError("El tiempo debe ser un valor positivo y representar una marca válida.")
        self.mejores_tiempos.append(tiempo)


if __name__ == "__main__":
    # Script mínimo 
    registro = Registro()

    try:
        f1 = Futbolista("Ana", 20, "Rojo FC", 2, 1, "delantera")
        f2 = Futbolista("Luis", 22, "Azul FC", 1, 0, "defensa")
        t1 = Tenista("Marta", 19, "Sofía", 120)
        a1 = Atleta("Pedro", 25, "100m")

        registro.añadir_deportista(f1)
        registro.añadir_deportista(f2)
        registro.añadir_deportista(t1)
        registro.añadir_deportista(a1)
    except ValueError as exc:
        print(f"Error al registrar deportistas: {exc}")

    print("\n--- Buscar deportista ---")
    print(registro.buscar_deportista("Ana"))
    print(registro.buscar_deportista("NoExiste"))

    competencia_futbol = Competencia(
        nombre="Torneo Apertura",
        fecha=date.today(),
        participantes=[],
        resultados={},
        deporte="Fútbol",
        registro=registro,
    )

    try:
        competencia_futbol.inscribir_participante(f1)
        competencia_futbol.inscribir_participante(f2)
        competencia_futbol.registrar_resultado({f1: 10, f2: 7})
    except ValueError as exc:
        print(f"Error en competencia: {exc}")

    print("\n--- Resultados competencia ---")
    competencia_futbol.mostrar_resultado()

    print("\n--- Ranking general ---")
    registro.mostrar_deportistas()

    print("\n--- Ranking por deporte: Fútbol ---")
    registro.mostrar_ranking_por_deporte("fútbol")
