import threed_optix.api as opt


SETUP_NAME = 'setup_a'
PART_LABEL = '110-0211E 25.4 mm Dia. x 60 mm FL; Uncoated; Plano-Convex Lens'


def main():
    api = opt.ThreedOptixAPI('e31aeeae-e9b0-436c-abba-735ee10cee8e')

    setups = api.get_setups()
    s = setups[0]
    for i in range(len(setups)):
        if setups[i].name == SETUP_NAME:
            s = setups[i]
            api.fetch(s)
            print(f"found setup {s}")

    if s.name != SETUP_NAME:
        print(f"setups {SETUP_NAME} not found")
        return

    parts = s.parts
    p = parts[0]
    for i in range(len(parts)):
        if parts[i].label == PART_LABEL:
            p = parts[i]
            api.fetch(p)
            print(f"found part {p}")

    if p.label != PART_LABEL:
        print(f"part {PART_LABEL} no found")

    print("run simulation")
    distance = -1
    for _ in range(60):
        print(p.pose)
        r = api.run(s)
        api.fetch(r)

        distance += 1
        result_file = f'example_0_sim_result_{distance}.csv'
        r.data.to_csv(result_file)

        p.pose.position.z += 1
        api.update(p)


if __name__ == '__main__':
    main()
