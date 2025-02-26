from BaseApp import BaseApp
from tkinter import ttk, messagebox

# Dicionário com as keywords e descrições completas
keywords = {
    "PRECISE": (
        "Non-LBFGS jobs: The criteria for terminating all optimizations, electronic and geometric, are to be increased by a factor, normally 100. "
        "This can be used where more precise results are wanted. If the results are going to be used in a FORCE calculation, where the geometry needs "
        "to be known quite precisely, then PRECISE is recommended; for small systems, the extra cost in CPU time is minimal. PRECISE is not recommended "
        "for experienced users; instead, GNORM=n.nn and SCFCRT=n.nn or RELSCF=n.nn are suggested. PRECISE should only rarely be necessary in a FORCE calculation: "
        "all it does is remove quartic contamination, which only affects the trivial modes significantly, and is very expensive in CPU time. "
        "LBFGS jobs: In the LBFGS procedure, if PRECISE is present then the number of cycles used in identifying the lowest-energy system is increased from 30 to 60. "
        "See also LET."
    ),
    "PULAY": (
        "The default converger in the SCF calculation is to be replaced by Pulay's procedure as soon as the density matrix is sufficiently stable. "
        "A considerable improvement in speed can frequently be achieved by the use of PULAY, particularly for excited states. If a large number of SCF calculations "
        "are envisaged, a sample calculation using 1SCF and PULAY should be compared with using 1SCF on its own, and if a saving in time results, then PULAY should be used "
        "in the full calculation. PULAY should be used with care in that its use will prevent the combined package of convergers (SHIFT, PULAY and the CAMP-KING convergers) "
        "from being used automatically in the event that the system fails to go SCF in (ITRY-10) iterations.\n\n"
        "PULAY does not work with MOZYME.\n\n"
        "The combined set of convergers very seldom fails."
    ),
    "CAMP": (
        "The Camp-King converger is to be used. This is a very powerful, but CPU intensive, SCF converger.  The Camp-King converger does not work with MOZYME."
    ),
    "MOZYME": (
        "The keyword MOZYME replaces the standard SCF procedure with a localized molecular orbital (LMO) method. MOZYME was developed to allow very large organic compounds, "
        "specifically enzymes, to be easily calculated. The time required for a SCF calculation increases approximately linearly with the size of the system, see literature on MOZYME "
        "and Modeling proteins. MOZYME jobs do not run faster when a GPU chip is used.\n\n"
        "Notes, warnings and cautions concerning MOZYME calculations:\n"
        "Although a job that uses the MOZYME technique should give results that are the same as conventional SCF calculations, in practice there are differences. Most of these differences "
        "are small, but in some jobs the differences between MOZYME and conventional SCF calculations, particularly the calculation of ΔHf, can be significant. A single point calculation using "
        "MOZYME and conventional methods would produce essentially the same ΔHf, and for the purposes of this discussion the results of a single SCF calculated by both methods can be regarded as "
        "being identical. The problem with different ΔHf occurs when multiple SCF calculations are performed, this is the situation in a geometry optimization or reaction path calculation. In such "
        "calculations, the LMOs that result from an SCF calculation are used as starting LMOs in the next SCF calculation. In the first SCF calculation, the starting LMOs are exact - they form rigorously "
        "orthonormal sets, one for the occupied and one for the virtual sets. At the end of the SCF, small errors arising from truncation of the LMOs and incomplete pairwise rotations give rise to a small "
        "degradation of the orthonormal nature of the LMOs. In a single SCF, this degradation is unimportant, but when many SCF calculations are done, the loss of orthonormality increases steadily. This manifests "
        "itself as an error in the calculated ΔHf and to a much smaller extent in the gradients, and therefore, by implication, in the geometry. The loss of orthonormality could be corrected by re-orthogonalizing "
        "the LMOs, but the CPU cost of this is great, and re-othogonalization is not done by default, although it can be done if desired using REORTHOG. Fortunately, a very simple procedure exists to completely correct "
        "this error: After any long run involving many MOZYME SCF calculations, use the final geometry generated as the starting point for a 1SCF calculation, and then use the ΔHf from that calculation. This strategy "
        "should be used:\n\n"
        "(A) In global optimizations.\n"
        "(B) In transition state location runs.\n"
        "(C) At the end of IRC runs.\n\n"
        "Do not use OLDENS as that would re-use the now-inaccurate sets of LMOs, and thus defeat the purpose of doing the 1SCF calculation. As mentioned above, the errors in the gradient are small, so the geometry is essentially "
        "unaffected by the loss of orthonormality. However, it is still a good practice to optimize geometries in three or more separate runs, if only to provide an opportunity to check that the calculation is proceeding as intended.\n\n"
        "During geometry optimizations, the error in ΔHf caused by the deterioration of the LMOs can result in the energy rising near the end of the run. If this happens, the lowest energy structure will be output, instead of the last structure calculated.\n\n"
        "By default, the M.O.s printed are LMOs. If canonical M.O.s are needed, use keyword EIGEN. EIGEN uses a large amount of memory and might not work if the system is too large. Even if it does work, it might take a lot of CPU time, so EIGEN should only be used with 1SCF.\n\n"
        "Limitations of MOZYME:\n"
        "Only closed shell RHF calculations are allowed. This means that MOZYME calculations are limited to species in their ground state. Radicals and electronic excited states cannot be run. "
        "Ions that are definitely open-shell, such as Cr(III), cannot be run. Only pre-set oxidation states are allowed, e.g. CIV and AuI. Oxidation states of metals can be changed using the METAL keyword, e.g. METAL=(Au(+3)). "
        "The results are not so precise, so for runs that need high precision (such as FORCE calculations), MOZYME is discouraged. For proteins in particular, use a larger gradient norm criterion, e.g. GNORM=5, this will reduce the "
        "possibility of convergence failure."
    ),
    "LET": (
        "As MOPAC evolves, the meaning of LET is changing.\n\n"
        "Now LET means essentially 'I know what I'm doing, override safety checks'.\n\n"
        "Currently, LET has the following meanings:\n"
        "1. In a FORCE calculation, it means that the supplied geometry is to be used, even if the gradients are large.\n"
        "2. In a geometry optimization, the specified GNORM is to be used, even if it is less than 0.01.\n"
        "3. In a POLAR calculation, the molecule is to be orientated along its principal moments of inertia before the calculation starts. LET will prevent this step being done.\n"
        "4. In an EF calculation, allow the ΔHf to rise. This allows reaching the gradient minimum, which is a well-defined point.\n"
        "5. When comparing protein geometries, it means that hydrogen atoms on different residues are paired up.\n"
        "6. In a LOCATE-TS calculation, do not perform a comparison of the reactants and products. Useful for small systems.\n"
        "7. In an LBFGS calculation, the default number of cycles used in identifying the lowest-energy geometry is increased from 30 to 60. "
        "Other values can be set using LET(nnn), where 'nnn' is the number of cycles."
    ),
    "FORCE": (
        "A force-calculation is to be run. The Hessian, that is the matrix in millidynes per Ångstrom of second derivatives of the energy with respect to "
        "displacements of all pairs of atoms in x, y, and z directions, is calculated. On diagonalization this gives the force constants for the molecule. "
        "The force matrix, weighted for isotopic masses, is then used for calculating the vibrational frequencies. The system can be characterized as a ground "
        "state or a transition state by the presence of five (for a linear system) or six eigenvalues which are very small (less than about 30 reciprocal centimeters). "
        "A transition state is further characterized by one, and exactly one, negative force constant."
    ),
    "FORCETS": (
       "Calculating the Hessian for a large system takes a long time, and often the only reason for running a FORCE calculation is to verify that the system is a transition state. "
       "To speed up this calculation, FORCETS is provided. The FORCETS calculation builds a Hessian for the atoms involved in the transition state, that is, all atoms with optimization flags "
       "of '1' or '2' (For the meaning of '2', see MINI). All atoms used in building the Hessian matrix must be at the start of the geometry. "
       "This Hessian will be used in generating vibrations for the transition state. If the system is a genuine transition state, then there will be one imaginary vibration, "
       "indicated in the output as a 'negative' vibration. Its value will be within a few percent of the value that would be obtained if a full calculation were done. "
       "The imaginary vibration should involve the atom(s) that move during the reaction. All other vibrations should be positive, but their value is not useful, "
       "because they would involve atoms other than those in the transition state."
    ),
    "NOREOR": (
       "When the symmetry of a molecule is being worked out, the molecule is orientated by default. If NOREOR is specified, the molecule will not be reorientated. "
       "The main reason to not reorientate the molecule is to allow a lower point-group to be used, and to allow the x and y axes in Abelian groups to be defined by the user. "
       "When GEO_REF is used, the default is that the reference geometry is rotated and translated to give the maximum overlap with the data-set geometry. "
       "This operation will be suppressed when NOREOR is present. "
       "In a FORCE calculation, NOREOR will prevent the molecules being reoriented to line up the moment of inertia axes with the Cartesian axes."
    ),
    "ISOTOPE": (
        "Generation of the FORCE matrix is very time-consuming, and in isotopic substitution studies several vibrational calculations may be needed. "
        "To allow the frequencies to be calculated from the (constant) force matrix, ISOTOPE is used. When a FORCE calculation is completed, ISOTOPE will cause the force matrix to be stored, "
        "regardless of whether or not any intervening restarts have been made. To re-calculate the frequencies, etc., starting at the end of the force matrix calculation, specify RESTART. "
        "The two keywords RESTART and ISOTOPE can be used together. For example, if a normal FORCE calculation runs for a long time, the user may want to divide it up into stages and save the final force matrix. "
        "Once ISOTOPE has been used, it does not need to be used on subsequent RESTART runs. ISOTOPE can also be used with FORCE to set up a RESTART file for an IRC=n calculation."
    ),
    "GNORM=n.nn": (
        "The geometry optimization termination criteria (see Criteria) in both gradient minimization and energy minimization can be over-ridden by specifying a gradient norm requirement. "
        "For example, GNORM=20 would allow the geometry optimization to exit as soon as the gradient norm dropped below 20.0 kcal/mol/Ångstrom, the default being 1.0. "
        "For proteins and solids, i.e., large systems, GNORM=10 should be used. Lower values might work, but there is an increased risk of the heat of formation not decreasing, "
        "and all that happens is that CPU time is wasted. "
        "For small system high-precision work, GNORM=0.0 is recommended. Unless LET is also used, the GNORM will be set to the larger of 0.01 and the specified GNORM. "
        "Results from GNORM=0.01 are easily good enough for all high-precision work. "
        "N.b.: Do not confuse GNORM, the keyword, with GNORM, the value of the scalar of the calculated gradient. "
        "The keyword GNORM defines the criterion for an optimized geometry, GNORM is the value calculated during a geometry optimization, and is printed in the output at the end of each cycle. "
        "When GNORM drops below the level set by GNORM=n.nn, the geometry optimization will terminate."
    ),
    "SCFCRT=n.nn": (
        "SCFCRT sets the self-consistent field criterion, i.e., the change in energy in kcal/mol on two successive iterations. "
        "For most situations where the SCF criterion needs to be modified, use RELSCF instead. RELSCF is useful if the value of the default SCF criterion is not readily available, "
        "as for example when PRECISE or any other keywords that modify the SCF criterion are used. "
        "The default SCF criterion, 1x10⁻⁴ kcal/mol, is to be replaced by that defined by SCFCRT=n.nnn. Other criteria may make the requirements for an SCF slightly more stringent. "
        "The SCF criterion can be varied from about 1.0 to 1.D-25, although numbers in the range 0.1 to 1.D-9 will suffice for most applications. "
        "In FORCE, NLLSQ, SIGMA, or TS calculations, the default value of SCFCRT is 1x10⁻⁷. Be careful in FORCE calculations - high precision is needed; "
        "if high precision is not used, the vibrational frequencies might be wrongly predicted. "
        "An overly tight criterion can lead to failure to achieve an SCF, and the consequent failure of the run. See also RELSCF."
    ),
    "RELSCF": (
        "When RELSCF=n is present, the default SCF criterion is multiplied by n. "
        "This is useful if the value of the default SCF criterion is not readily available, as for example when PRECISE or any other keywords that modify the SCF criterion are used. "
        "Examples: RELSCF=10 will make the SCF test easier to pass—the criterion will be made 10 times easier. "
        "Similarly, if the results are not precise enough, then RELSCF=0.1 would increase the precision 10 times. "
        "However, if the precision is increased too much, the SCF test might never be passed. See also SCFCRT."
    ),
    "LBFGS": (
        "Optimize the geometry using the L-BFGS function minimizer. This is based on the BFGS optimizer, but it does not store the inverse Hessian, "
        "instead it is calculated as needed. Because of this, the L-BFGS method uses very little storage, and is therefore suitable for optimizing very large systems. "
        "The L-BFGS optimizer is the default if 100 or more variables are to be optimized. For such systems, L-BFGS is more efficient than Baker's Eigenfollowing, "
        "however, there is no guarantee that the L-BFGS method will produce a minimum energy. In systems where two or more species are present, and only low-energy interactions "
        "bind the species together, the L-BFGS optimizer sometimes fails to produce a minimum energy system. If this happens, or if for any other reason the L-BFGS is not wanted, "
        "add keyword EF or BFGS. Both these methods are more reliable for difficult systems.\n\n"
        "Note on use of L-BFGS with large systems, particularly proteins:\n"
        "The L-BFGS optimization method does not explicitly minimize the heat of formation (ΔHf), therefore it is possible for the ΔHf to rise from one cycle to the next, "
        "particularly near the end of a geometry optimization run. Since the objective of geometry optimization is finding the lowest-energy geometry, terminating an optimization "
        "with a structure that is not the lowest-energy calculated is not acceptable. This fault most often occurs in large systems, especially in proteins, and to avoid it, "
        "the optimization procedure has been modified as follows:\n\n"
        "During a geometry optimization using L-BFGS, the system with the lowest ΔHf is stored. At the beginning of a job, the ΔHf is calculated and stored along with the starting geometry. "
        "After each cycle, the ΔHf is compared with the stored value. If it is lower, the store is updated with the new geometry and ΔHf, ensuring that the stored values are always the best found. "
        "At the end of the run, if the working geometry has a higher ΔHf than the stored geometry, it will be replaced with the stored geometry, and the final output will refer to this geometry.\n\n"
        "This workaround is applied to all jobs using L-BFGS that end normally, run out of time, or are stopped using SHUT. "
        "Warning: If a large job is restarted using RESTART and 1SCF is specified, this workaround will not be used. For large jobs where 1SCF is needed and there is a risk that the "
        "ΔHf in the <file>.RES file is not the lowest calculated, use the final geometry from the output file of the previous run.\n\n"
        "The default number of cycles for deciding if the ΔHf is at a minimum is 30. This is reset to 60 if PRECISE is used, or to another value if LET(nnn) is used. "
        "This option is useful when there is a risk of the optimization stopping too far from the minimum.\n\n"
        "For most jobs, the final geometry will be the best, and this workaround will not be needed, but if the lowest-energy geometry is not the last geometry calculated by L-BFGS, "
        'then the message: "CURRENT BEST VALUE OF HEAT OF FORMATION" will be printed.\n\n'
        "Notes on the L-BFGS optimization method:\n"
        "The L-BFGS optimization procedure is a limited-memory variation of the Broyden-Fletcher-Goldfarb-Shanno (BFGS) quasi-Newton algorithm. "
        "Rather than storing the Hessian, the L-BFGS method stores only the gradient vectors for the last few geometries calculated. In MOPAC, a maximum of 12 gradient vectors are stored. "
        "It then uses these vectors to approximate individual elements of the Hessian as needed. This method is well-suited for large systems such as proteins, macromolecules, and solids. "
        "In practice, it is also the best geometry optimizer for systems of thirty or more atoms. More details on the L-BFGS method can be found online.\n\n"
        "It uses the gradient only, by moving the atoms in the system in the downhill direction. Although the L-BFGS method does not use the ΔHf explicitly, for most systems it minimizes "
        "ΔHf as a side effect of minimizing the gradient. While not explicitly stated in the algorithm, L-BFGS optimizes the geometry to a ground state. "
        "There is no known case where it has optimized an unconstrained geometry to a transition state.\n\n"
        "Using only the gradient and not the ΔHf has advantages: when L-BFGS makes a bad step, it uses the results to determine a better step, leading to a more rapid descent "
        "to a stationary point on the Potential Energy Surface."
    )
}

class KeywordsApp(BaseApp):
    """Classe para exibir as keywords"""
    def __init__(self):
        super().__init__("Keywords")

        header = ttk.Label(self, text="Select the Keyword", font=("Helvetica", 16, "bold"), background="#f8f9fa")
        header.pack(pady=20)

        frame = ttk.Frame(self, padding=10)
        frame.pack(expand=True)

        # Criando botões para todas as keywords do dicionário
        for keyword in keywords.keys():
            btn = ttk.Button(frame, text=keyword, command=lambda k=keyword: self.mostrar_descricao(k), width=20)
            btn.pack(pady=5)

    def mostrar_descricao(self, keyword):
        descricao = keywords.get(keyword, "Descrição não encontrada.")
        messagebox.showinfo(title=keyword, message=descricao)

if __name__ == "__main__":
    app = KeywordsApp()
    app.mainloop()
    